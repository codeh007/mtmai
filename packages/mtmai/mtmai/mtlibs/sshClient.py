import logging
import os
import stat

import paramiko

logger = logging.getLogger()


class SshClient:
    def __init__(self, host, user="root", password=None, port=22, timeout=30):
        """如果没有指定密码，就使用私钥登陆"""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        # 设置 paramiko的一些环境
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.timeout = timeout
        self.t = paramiko.Transport(sock=(self.host, self.port))

    def _password_connect(self):
        # self.client.set_missing_host_key_policy(paramiko.)
        self.client.connect(
            hostname=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            allow_agent=False,
        )
        self.t.connect(
            username=self.user, password=self.password
        )  # sptf 远程传输的连接
        # logger.debug("ssh 密码连接成功？")

    def _key_connect(self):
        # 建立连接
        # self.pkey = paramiko.RSAKey.from_private_key_file('/home/roo/.ssh/id_rsa', )
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=self.host,
            port=self.port,
            username=self.user,
        )  # pkey=self.pkey)
        self.t.connect(
            username=self.user,
        )  # pkey=self.pkey)

    def connect(self):
        # self.client.connect(host,port=port, username=user, password=password)
        try:
            self._key_connect()
        except:
            logger.debug("ssh key connect failed, trying to password connect...")
            try:
                self._password_connect()
            except Exception as e:
                logger.exception(e)
                logger.debug(f"ssh password connect fail, to host {self.host} ")
                return False

        return True

    def close(self):
        self.t.close()
        self.client.close()

    def exec_cmd(self, script):
        """执行命令，返回执行结果"""
        stdin, stdout, stderr = self.client.exec_command(script)

        res, err = stdout.read(), stderr.read()
        # result = res if res else err
        # return result.decode()
        return (res.decode(), err.decode())

    def uploadFiles(self, file_from, file_to):
        trans = paramiko.Transport((self.host, self.port))
        trans.connect(username=self.user, password=self.password)
        # 建立一个sftp客户端对象，通过ssh transport操作远程文件
        sftp = paramiko.SFTPClient.from_transport(trans)
        # Copy a local file (localpath) to the SFTP server as remotepath
        sftp.put(file_from, file_to)
        trans.close()

    def downloadFile(self, remote_path, local_path):
        # TODO:
        logging.log("downloadFile 功能未实现")

    def portMap(self, local_port, remote_ip, remote_port):
        # 端口映射
        import select
        from threading import Thread

        try:
            import SocketServer
        except ImportError:
            import socketserver as SocketServer

        class ForwardServer(SocketServer.ThreadingTCPServer):
            daemon_threads = True

        allow_reuse_address = True

        class Handler(SocketServer.BaseRequestHandler):
            def handle(self):
                try:
                    chan = self.ssh_transport.open_channel(
                        "direct-tcpip",
                        (self.chain_host, self.chain_port),
                        self.request.getpeername(),
                    )
                except Exception as e:
                    logging.log(
                        "Incoming request to %s:%d failed: %s"
                        % (self.chain_host, self.chain_port, repr(e))
                    )
                    return
                if chan is None:
                    logging.log(
                        "Incoming request to %s:%d was rejected by the SSH server."
                        % (self.chain_host, self.chain_port)
                    )
                    return

                while True:
                    r, w, x = select.select([self.request, chan], [], [])
                    if self.request in r:
                        data = self.request.recv(1024)
                        if len(data) == 0:
                            break
                        chan.send(data)
                    if chan in r:
                        data = chan.recv(1024)
                        if len(data) == 0:
                            break
                        self.request.send(data)

                self.request.getpeername()
                chan.close()
                self.request.close()

        def forward_tunnel(local_port, remote_host, remote_port, transport):
            class SubHander(Handler):
                chain_host = remote_host
                chain_port = remote_port
                ssh_transport = transport

            ForwardServer(("", local_port), SubHander).serve_forever()

        tunnel_thread = Thread(
            target=forward_tunnel,
            args=(local_port, remote_ip, remote_port, self.client.get_transport()),
        )
        tunnel_thread.start()
        print("线程启动了")

    # def execute_cmd(self, cmd):

    #     stdin, stdout, stderr = self.ssh.exec_command(cmd)

    #     res, err = stdout.read(), stderr.read()
    #     result = res if res else err

    #     return result.decode()

    # 从远程服务器获取文件到本地
    def sftp_get(self, remotefile, localfile):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.get(remotefile, localfile)

    # 从本地上传文件到远程服务器
    def sftp_put(self, localfile, remotefile):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.put(localfile, remotefile)

    # 递归遍历远程服务器指定目录下的所有文件
    def _get_all_files_in_remote_dir(self, sftp, remote_dir):
        all_files = list()
        if remote_dir[-1] == "/":
            remote_dir = remote_dir[0:-1]

        files = sftp.listdir_attr(remote_dir)
        for file in files:
            filename = remote_dir + "/" + file.filename

            if stat.S_ISDIR(file.st_mode):  # 如果是文件夹的话递归处理
                all_files.extend(self._get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)

        return all_files

    def sftp_get_dir(self, remote_dir, local_dir):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.t)

            all_files = self._get_all_files_in_remote_dir(sftp, remote_dir)

            for file in all_files:
                local_filename = file.replace(remote_dir, local_dir)
                local_filepath = os.path.dirname(local_filename)

                if not os.path.exists(local_filepath):
                    os.makedirs(local_filepath)

                sftp.get(file, local_filename)
        except Exception as e:
            logger.exception(e)

    # 递归遍历本地服务器指定目录下的所有文件
    def _get_all_files_in_local_dir(self, local_dir):
        all_files = list()

        for root, dirs, files in os.walk(local_dir, topdown=True):
            for file in files:
                filename = os.path.join(root, file)
                all_files.append(filename)

        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.t)

            if remote_dir[-1] == "/":
                remote_dir = remote_dir[0:-1]

            all_files = self._get_all_files_in_local_dir(local_dir)
            for file in all_files:
                remote_filename = file.replace(local_dir, remote_dir)
                remote_path = os.path.dirname(remote_filename)

                try:
                    sftp.stat(remote_path)
                except:
                    # os.popen('mkdir -p %s' % remote_path)
                    self.execute_cmd(
                        "mkdir -p %s" % remote_path
                    )  # 使用这个远程执行命令

                sftp.put(file, remote_filename)

        except Exception as e:
            logger.debug(e)
