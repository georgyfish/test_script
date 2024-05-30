#!/usr/bin/env python3

import paramiko,logging,sys
from paramiko import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError
from logManager import logManager

class sshClient():

    def __init__(self, hostname, username, password, port=22):
        self.client = paramiko.SSHClient()
        self.log = logManager('ssh')
        self.host = hostname       #连接的目标主机
        self.port = port      #指定端口
        self.user = username      #验证的用户名
        self.passwd = password      #验证的用户密码

    def login(self, timeout=10):
        self.log.logger.info(f"Connect to '{self.user}@{self.host}/{self.port}' PassWd: {self.passwd}")
        try:
            # 设置允许连接known_hosts文件中的主机（默认连接不在known_hosts文件中的主机会拒绝连接抛出SSHException）
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, port=self.port, username=self.user, password=self.passwd, timeout=timeout)
        except AuthenticationException:
            self.log.logger.error("username or password error")
            return 1001
        except NoValidConnectionsError:
            self.log.logger.error(f"Unable to connect to {self.host}/{self.port}")
            return 1002
        except:
            # print("Unexpected error:", sys.exc_info()[0])
            self.log.logger.error(f"Unexpected error: {sys.exc_info()[0]}")
            return 1003
        return 1000

    def execute(self, command, timeout=10):
        self.log.logger.info(f'Execute "{command}"')
        result = ""
        stdin, stdout, stderr = self.client.exec_command(command)
        # stdout为缓冲区，数据都取之后清空
        result = stdout.read().decode().strip('\n')
        # self.log.logger.info(f"Result: \n{result}")
        # print(f"stderr={stderr},type={type(stderr)}")
        # print(f"stderr={stderr.read()},type={type(stderr.read())}")
        if  stderr.read().decode() != '' and stderr.read().decode() != None:
            self.log.logger.warning(stderr.read().decode().strip("\n"))
            # print(f"stderr.read().decode()={stderr.read().decode()}hhh")
        return result   # .replace("\n", " ").strip().split(" ")

    def logout(self):
        self.log.logger.info(f"Close connect '{self.host}/{self.port}'")
        self.client.close()

if __name__ == '__main__':
    Pc = sshClient("192.168.114.8","swqa","gfx123456")
    if 1000 == Pc.login():
        # result = Pc.execute("wget https://oss.mthreads.com/product-release/develop/20240529/musa_2024.05.29-D+11244+dkms+glvnd-Ubuntu_amd64.deb -O 1.deb")
        result = Pc.execute("sudo grep 'Driver Version' /sys/kernel/debug/musa/version|awk -F[ '{print $NF}'|awk -F] '{print $1}'")
        # print(type(Pc))
        print(f"result={result},type={type(result)}")
        # for line in result.splitlines():
        #     if "Version: " in line:
        #         deb_version = line.split("Version: ")[-1]
        # print(deb_version)
        Pc.logout()