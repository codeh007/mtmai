import logging
import os
import stat
import traceback

import paramiko

logger = logging.getLogger()
"""
使用paramiko类实现ssh的连接登陆,以及远程文件的上传与下载, 基本远程命令的实现等
"""


class SSH:
    def __init__(self, ip, port=22, username=None, password=None, timeout=30):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

        self.ssh = paramiko.SSHClient()

        self.t = paramiko.Transport(sock=(self.ip, self.port))

    def _password_connect(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=self.ip, port=22, username=self.username, password=self.password
        )
        self.t.connect(
            username=self.username, password=self.password
        )  # sptf 远程传输的连接

    def _key_connect(self):
        # 建立连接
        # self.pkey = paramiko.RSAKey.from_private_key_file('/home/roo/.ssh/id_rsa', )
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=self.ip, port=22, username=self.username, pkey=self.pkey
        )
        self.t.connect(username=self.username, pkey=self.pkey)

    def connect(self):
        try:
            self._key_connect()
        except:
            print("ssh key connect failed, trying to password connect...")
            try:
                self._password_connect()
            except Exception as e:
                logger.exception(e)
                logger.warning("密码登录ssh失败")
                # print('ssh password connect faild!')

    def close(self):
        self.t.close()
        self.ssh.close()

    def execute_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        res, err = stdout.read(), stderr.read()
        result = res if res else err

        return result.decode()

    # 从远程服务器获取文件到本地
    def _sftp_get(self, remotefile, localfile):
        sftp = paramiko.SFTPClient.from_transport(self.t)
        sftp.get(remotefile, localfile)

    # 从本地上传文件到远程服务器
    def _sftp_put(self, localfile, remotefile):
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
        except:
            print("ssh get dir from master failed.")
            print(traceback.format_exc())

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

        except:
            print("ssh get dir from master failed.")
            print(traceback.format_exc())


if __name__ == "__main__":
    ssh = SSH(
        ip="192.168.0.10", username="rpl", password="12345678"
    )  # 创建一个ssh类对象

    ssh.connect()  # 连接远程服务器

    cmd = "ls -lh"
    ssh.execute_cmd(cmd)  # 执行命令

    remotefile, local_file = "xxx", "xxx"
    ssh.sftp_get(remotefile, local_file)  # 下载文件

    remotedir, localdir = "xxx", "xxx"
    ssh.sftp_put_dir(localdir, remotedir)  # 上传文件夹
    ssh.close()
