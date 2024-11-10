//! SSH types and methods.

use std::borrow::Cow;
use std::error::Error;
use std::io::{self, ErrorKind, Read, Write};
use std::net::{SocketAddr, TcpStream, ToSocketAddrs};
use std::path::{Path, PathBuf};
use std::time::Duration;
use std::{fs, mem};

use crate::auth::{Auth, AuthMethod};
use pyo3::exceptions::{
    PyConnectionRefusedError, PyException, PyFileExistsError, PyFileNotFoundError, PyIOError,
    PyPermissionError, PyValueError,
};
use pyo3::prelude::*;
use ssh2::{Channel, ErrorCode, OpenFlags, OpenType, Session, Sftp, Stream};

/// Default SSH port.
const DEFAULT_PORT: u16 = 22;
/// Default connection timeout.
const DEFAULT_TIMEOUT: u64 = 30;

// Custom Python exception types.
pyo3::create_exception!(russhy, SessionException, PyException);
pyo3::create_exception!(russhy, SFTPException, PyException);
pyo3::create_exception!(russhy, SSHException, PyException);

/// Convenience function to map Rust errors to appropriate Python exceptions.
///
/// This function can be passed to [`Result::map_err`].
///
/// # Arguments
///
/// * `err` - The error to convert.
fn excp_from_err<E>(err: E) -> PyErr
where
    E: Error + Send + Sync + 'static,
{
    let err: Box<dyn Error> = Box::new(err);

    if let Some(ssh_err) = err.downcast_ref::<ssh2::Error>() {
        return match ssh_err.code() {
            ErrorCode::Session(_) => SessionException::new_err(ssh_err.to_string()),
            ErrorCode::SFTP(_) => SFTPException::new_err(ssh_err.to_string()),
        };
    }

    if let Some(io_err) = err.downcast_ref::<io::Error>() {
        return match io_err.kind() {
            ErrorKind::AlreadyExists => PyErr::new::<PyFileExistsError, _>(io_err.to_string()),
            ErrorKind::NotFound => PyErr::new::<PyFileNotFoundError, _>(io_err.to_string()),
            ErrorKind::PermissionDenied => PyErr::new::<PyPermissionError, _>(io_err.to_string()),
            ErrorKind::ConnectionRefused => {
                PyErr::new::<PyConnectionRefusedError, _>(io_err.to_string())
            }
            _ => PyErr::new::<PyIOError, _>(io_err.to_string()),
        };
    }

    PyErr::new::<PyException, _>(err.to_string())
}

#[pyclass]
/// Represents the output produced when running [`SSHClient::exec_command`].
pub struct ExecOutput {
    channel: Option<Channel>,
    /// The `stdin` stream.
    stdin: Option<Stream>,
    /// The `stdout` stream's contents.
    stdout: Option<Stream>,
    /// The `stderr` stream's contents.
    stderr: Option<Stream>,
}

#[pymethods]
impl ExecOutput {
    /// Writes the provided data to the `stdin` stream and closes it.
    ///
    /// **NOTE**: Future calls will discard the provided data without doing anything.
    ///
    /// # Arguments
    ///
    /// * `data` - The data to write to the stream.
    pub fn write_stdin(&mut self, data: &[u8]) -> PyResult<()> {
        if let Some(mut stdin) = self.stdin.take() {
            if let Some(channel) = self.channel.as_mut() {
                stdin.write_all(data).map_err(excp_from_err)?;
                stdin.flush().map_err(excp_from_err)?;

                channel.send_eof().map_err(excp_from_err)?;
            }
        }

        Ok(())
    }

    /// Reads the contents of the `stdout` stream and consumes it.
    ///
    /// **NOTE**: Future calls will return an empty string.
    fn read_stdout(&mut self) -> PyResult<Cow<[u8]>> {
        let mut buf = Vec::new();

        if let Some(mut stdout) = self.stdout.take() {
            stdout.read_to_end(&mut buf).map_err(excp_from_err)?;
        }

        Ok(Cow::from(buf))
    }

    /// Reads the contents of the `stderr` stream and consumes it.
    ///
    /// **NOTE**: Future calls will return an empty string.
    fn read_stderr(&mut self) -> PyResult<Cow<[u8]>> {
        let mut buf = Vec::new();

        if let Some(mut stderr) = self.stderr.take() {
            stderr.read_to_end(&mut buf).map_err(excp_from_err)?;
        }

        Ok(Cow::from(buf))
    }

    /// Retrieves the exit status of the command and closes the channel and all streams.
    ///
    /// **NOTE**: Future calls will return 0.
    ///
    /// **NOTE**: Future reads of the `stdout` or `stderr` streams will return empty strings.
    fn exit_status(&mut self) -> PyResult<i32> {
        let mut exit_status = 0;

        if let Some(mut chan) = self.channel.take() {
            let mut stdout = String::new();
            let mut stderr = String::new();

            chan.read_to_string(&mut stdout).map_err(excp_from_err)?;
            chan.stderr()
                .read_to_string(&mut stderr)
                .map_err(excp_from_err)?;

            chan.wait_close().map_err(excp_from_err)?;
            exit_status = chan.exit_status().map_err(excp_from_err)?;
        }

        Ok(exit_status)
    }

    /// Consumes all streams and closes the underlying channel if it exists and is active.
    ///
    /// If there is no active channel, then this function does nothing.
    fn close(&mut self) -> PyResult<()> {
        self.stdin.take();
        self.stdout.take();
        self.stderr.take();

        if let Some(mut channel) = self.channel.take() {
            channel.close().map_err(excp_from_err)?;
        }

        Ok(())
    }
}

/// Convenience function that concatenates a base and a child path into a [`PathBuf`].
///
/// If the base is `None`, the child path is returned as a [`PathBuf`].
///
/// # Arguments
///
/// * `base` - Optional base path.
/// * `path` - The child path.
fn path_from_base(base: Option<&Path>, path: impl AsRef<Path>) -> PathBuf {
    if let Some(base) = base {
        return base.join(path);
    }

    path.as_ref().to_path_buf()
}

#[pyclass]
/// A file on a remote server.
pub struct File(pub ssh2::File);

#[pymethods]
impl File {
    /// Reads and returns the contents of the file.
    pub fn read(&mut self) -> PyResult<Cow<[u8]>> {
        let mut buf = Vec::new();
        self.0.read_to_end(&mut buf).map_err(excp_from_err)?;

        Ok(Cow::from(buf))
    }

    /// Writes the specified data to the file.
    ///
    /// # Arguments
    ///
    /// * `data` - The data to write to the file.
    pub fn write(&mut self, data: &[u8]) -> PyResult<()> {
        self.0.write_all(data).map_err(excp_from_err)?;
        self.0.flush().map_err(excp_from_err)
    }
}

#[pyclass]
/// The SFTP client.
pub struct SFTPClient {
    /// Underlying SFTP client.
    client: Option<Sftp>,
    /// Current working directory.
    cwd: Option<PathBuf>,
}

#[pymethods]
impl SFTPClient {
    /// Changes the current working directory to the specified directory.
    ///
    /// If the specified directory is `None`, then the current working directory is unset.
    ///
    /// Once the current working directory is set, all SFTP operations will be relative to this path.
    ///
    /// **NOTE**: SFTP does not have a concept of a "current working directory", and so, this function
    /// tries to emulate it. Currently, only **absolute** paths are supported. This *MAY* change in the
    /// future, but is not guaranteed.
    ///
    /// # Arguments
    ///
    /// * `dir` - The directory to change to.
    #[pyo3(signature = (dir=None))]
    pub fn chdir(&mut self, dir: Option<PathBuf>) -> PyResult<()> {
        if let Some(client) = self.client.as_mut() {
            if let Some(path) = &dir {
                if client.opendir(path).is_err() {
                    return Err(excp_from_err(io::Error::new(
                        ErrorKind::NotFound,
                        format!("Path {} does not exist on server", path.display()),
                    )))?;
                }
            }

            self.cwd = dir;
        } else {
            return Err(SFTPException::new_err("SFTP session not open".to_string()));
        }

        Ok(())
    }

    /// Returns the current working directory.
    pub fn getcwd(&self) -> Option<PathBuf> {
        self.cwd.clone()
    }

    /// Creates a folder on the remote server with the specified numeric mode.
    ///
    /// # Arguments
    ///
    /// * `dir` The directory to create.
    /// * `mode` - POSIX-style permissions for the newly-created folder. Defaults to 511.
    #[pyo3(signature = (dir, mode=None))]
    pub fn mkdir(&mut self, dir: PathBuf, mode: Option<i32>) -> PyResult<()> {
        let mode = mode.unwrap_or(511);

        if let Some(client) = self.client.as_mut() {
            let path = path_from_base(self.cwd.as_deref(), &dir);
            return client.mkdir(&path, mode).map_err(excp_from_err);
        }

        Err(SFTPException::new_err("SFTP session not open".to_string()))
    }

    /// Removes a file from the remote server.
    ///
    /// **NOTE**: This only works for files. For directories, use [`SFTPClient::rmdir`].
    ///
    /// # Arguments
    ///
    /// * `path` - The path to the file to remove.
    pub fn unlink(&mut self, path: PathBuf) -> PyResult<()> {
        if let Some(client) = self.client.as_mut() {
            let path = path_from_base(self.cwd.as_deref(), path);
            return client.unlink(&path).map_err(excp_from_err);
        }

        Err(SFTPException::new_err("SFTP session not open".to_string()))
    }

    /// Removes a file from the remote server.
    ///
    /// **NOTE**: This method is just an alias to [`SFTPClient::unlink`] to mimic compatibility with paramiko.
    ///
    /// **NOTE**: This only works for files. For directories, use [`SFTPClient::rmdir`].
    ///
    /// # Arguments
    ///
    /// * `path` - The path to the file to remove.
    pub fn remove(&mut self, path: PathBuf) -> PyResult<()> {
        self.unlink(path)
    }

    /// Removes a directory from the remove server.
    ///
    /// **NOTE**: This only works for directories. For files, use [`SFTPClient::remove`].
    ///
    /// # Arguments
    ///
    /// * `dir` - The path to the directory to remove.
    pub fn rmdir(&mut self, dir: PathBuf) -> PyResult<()> {
        if let Some(client) = self.client.as_mut() {
            let path = path_from_base(self.cwd.as_deref(), dir);
            return client.rmdir(&path).map_err(excp_from_err);
        }

        Err(SFTPException::new_err("SFTP session not open".to_string()))
    }

    /// Opens a file on the remote server.
    ///
    /// # Arguments
    ///
    /// * `filename` - The name of the file (if file is in `cwd`) OR the path to the file.
    /// * `mode` - Python-style file mode.
    #[pyo3(signature = (filename, mode=None))]
    pub fn open(&mut self, filename: PathBuf, mode: Option<&str>) -> PyResult<File> {
        let flags = mode.unwrap_or("r");
        let flags = match flags {
            "r" | "rb" => OpenFlags::READ,
            "r+" => OpenFlags::READ | OpenFlags::WRITE,
            "w" | "wb" => OpenFlags::TRUNCATE | OpenFlags::WRITE,
            "w+" => OpenFlags::WRITE | OpenFlags::TRUNCATE | OpenFlags::READ,
            "a" | "ab" => OpenFlags::CREATE | OpenFlags::APPEND,
            "a+" => OpenFlags::CREATE | OpenFlags::APPEND | OpenFlags::READ | OpenFlags::WRITE,
            _ => return Err(PyValueError::new_err(format!("invalid mode: '{}'", flags))),
        };

        if let Some(client) = self.client.as_mut() {
            let path = path_from_base(self.cwd.as_deref(), filename);
            return Ok(File(
                client
                    .open_mode(&path, flags, 0o644, OpenType::File)
                    .map_err(excp_from_err)?,
            ));
        }

        Err(SFTPException::new_err("SFTP session not open".to_string()))
    }

    /// Opens a file on the remote server.
    ///
    /// **NOTE**: This method is just an alias to [`SFTPClient::open`] to mimic compatibility with paramiko.
    ///
    /// # Arguments
    ///
    /// * `filename` - The name of the file (if the file is in `cwd`) OR the path to the file.
    /// * `mode` - Python-style file mode.
    #[pyo3(signature = (filename, mode=None))]
    pub fn file(&mut self, filename: PathBuf, mode: Option<&str>) -> PyResult<File> {
        self.open(filename, mode)
    }

    /// Copies a file from the remote server to the local host.
    ///
    /// # Arguments
    ///
    /// * `remotepath` - The remote file path.
    /// * `localpath` - The local path to copy the file to.
    pub fn get(&mut self, remotepath: PathBuf, localpath: PathBuf) -> PyResult<()> {
        if let Some(client) = self.client.as_mut() {
            let remotepath = path_from_base(self.cwd.as_deref(), remotepath);

            let mut local = fs::File::open(localpath).map_err(excp_from_err)?;
            let mut remote = client.open(&remotepath).map_err(excp_from_err)?;

            io::copy(&mut remote, &mut local).map_err(excp_from_err)?;

            return Ok(());
        }

        Err(SFTPException::new_err("SFTP session not open".to_string()))
    }

    /// Copies a local file to the remote server.
    ///
    /// # Arguments
    ///
    /// * `localpath` - The path to the local file.
    /// * `remotepath` - The remote path to copy the file to.
    pub fn put(&mut self, localpath: PathBuf, remotepath: PathBuf) -> PyResult<()> {
        if let Some(client) = self.client.as_mut() {
            let remotepath = path_from_base(self.cwd.as_deref(), &remotepath);

            let mut local = fs::File::open(localpath).map_err(excp_from_err)?;
            let mut remote = client.create(&remotepath).map_err(excp_from_err)?;

            io::copy(&mut local, &mut remote).map_err(excp_from_err)?;

            return Ok(());
        }

        Err(SFTPException::new_err("SFTP session not open".to_string()))
    }

    /// Checks if the SFTP session is closed.
    pub fn is_closed(&self) -> bool {
        self.client.is_none()
    }

    /// Closes the SFTP session.
    pub fn close(&mut self) {
        self.client.take();
    }
}

#[pyclass]
#[derive(Default)]
/// The SSH client.
pub struct SSHClient {
    /// Established SSH session.
    sess: Option<Session>,
}

#[pymethods]
impl SSHClient {
    #[new]
    /// Creates a new [`SSHClient`].
    pub fn new() -> Self {
        Self::default()
    }

    /// Establishes an SSH connection and sets the created session on the client.
    ///
    /// # Arguments
    ///
    /// * `host` - The host name or address.
    /// * `auth` - The authentication method to use.
    /// * `username` - The SSH username. Defaults to root
    /// * `port` The SSH port. Defaults to 22.
    /// * `timeout` - The timeout for the TCP connection (in seconds). Defaults to 30.
    #[pyo3(signature = (host, auth, username=None, port=None, timeout=None))]
    pub fn connect(
        &mut self,
        host: String,
        auth: AuthMethod,
        username: Option<&str>,
        port: Option<u16>,
        timeout: Option<u64>,
    ) -> PyResult<()> {
        let port = port.unwrap_or(DEFAULT_PORT);
        let timeout = timeout.unwrap_or(DEFAULT_TIMEOUT);
        let addr: SocketAddr = (host, port)
            .to_socket_addrs()
            .map_err(excp_from_err)?
            .next()
            .ok_or(SSHException::new_err("SFTP server address not found"))?;

        let tcp = TcpStream::connect_timeout(&addr, Duration::from_secs(timeout))
            .map_err(excp_from_err)?;

        let mut sess = Session::new().map_err(excp_from_err)?;
        sess.set_tcp_stream(tcp);
        sess.handshake().map_err(excp_from_err)?;
        auth.authenticate(username.unwrap_or("root"), &mut sess)
            .map_err(excp_from_err)?;

        self.sess.replace(sess);

        Ok(())
    }

    /// Opens an SFTP session using the SSH session.
    ///
    /// Fails if there is no active SSH session (if [`SSHClient::connect`] was not called).
    pub fn open_sftp(&self) -> PyResult<SFTPClient> {
        if let Some(sess) = &self.sess {
            let client = Some(sess.sftp().map_err(excp_from_err)?);
            return Ok(SFTPClient { client, cwd: None });
        }

        Err(SessionException::new_err(
            "No active SSH session".to_string(),
        ))
    }

    /// Executes a command using the underlying session and returns the output.
    ///
    /// # Arguments
    ///
    /// * `command` - The command to run.
    /// * `detach` - do not wait for an output
    #[pyo3(signature = (command, detach=None))]
    pub fn exec_command(
        &self,
        command: String,
        detach: Option<bool>,
    ) -> PyResult<Option<ExecOutput>> {
        let mut stdin = None;
        let mut stdout = None;
        let mut stderr = None;
        let mut channel = None;

        if let Some(sess) = &self.sess {
            let mut chan = sess.channel_session().map_err(excp_from_err)?;
            chan.exec(&command).map_err(excp_from_err)?;

            if detach.unwrap_or(false) {
                mem::forget(chan);
                return Ok(None);
            }

            stdin = Some(chan.stream(0));
            stdout = Some(chan.stream(0));
            stderr = Some(chan.stderr());
            channel = Some(chan);
        }

        Ok(Some(ExecOutput {
            channel,
            stdin,
            stdout,
            stderr,
        }))
    }

    /// Invoke a shell
    ///
    /// # Notes
    ///
    /// This function currently doesn't return anything,
    /// it only allocates a pty and requests a shell from the server.
    pub fn invoke_shell(&self) -> PyResult<()> {
        if let Some(sess) = &self.sess {
            let mut chan = sess.channel_session().map_err(excp_from_err)?;
            chan.request_pty("vt100", None, None)
                .map_err(excp_from_err)?;
            chan.shell().map_err(excp_from_err)?;
        }

        Ok(())
    }

    pub fn authenticated(&self) -> bool {
        self.sess.as_ref().is_some_and(|sess| sess.authenticated())
    }

    /// Closes the underlying session.
    pub fn close(&mut self) {
        self.sess.take();
    }
}
