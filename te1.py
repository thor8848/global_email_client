#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:Administrator
@file: te1.py
@time: 2021/1/1  10:53
"""
import socks
from smtplib import SMTP, SMTP_SSL
import socket
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
# socks.set_default_proxy(socks.HTTP, '110.18.154.169', '13869')
# socket.socket = socks.socksocket
# s = socks.socksocket()
# s.set_proxy(socks.SOCKS5, "123.73.209.193", 32221)
# Can be treated like a regular socket object

# s.connect(("smtp.zmail300.cn", 25))
# s.send(b'helo [thor]')
# print(s.recv(4096))
class SocksSMTP(SMTP):

    def __init__(self,
                 host='',
                 port=0,
                 local_hostname=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                 source_address=None,
                 proxy_type=None,
                 proxy_addr=None,
                 proxy_port=None,
                 proxy_rdns=True,
                 proxy_username=None,
                 proxy_password=None,
                 socket_options=None):

        self.proxy_type = proxy_type
        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
        self.proxy_rdns = proxy_rdns
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.socket_options = socket_options
        # if proxy_type is provided then change the socket to socksocket
        # behave like a normal SMTP class.
        if self.proxy_type:
            self._get_socket = self.socks_get_socket

        super(SocksSMTP, self).__init__(host, port, local_hostname, timeout, source_address)

    def socks_get_socket(self, host, port, timeout):
        if self.debuglevel > 0:
            self._print_debug('connect: to', (host, port), self.source_address)
        return socks.create_connection((host, port),
                                       timeout=timeout,
                                       source_address=self.source_address,
                                       proxy_type=self.proxy_type,
                                       proxy_addr=self.proxy_addr,
                                       proxy_port=self.proxy_port,
                                       proxy_rdns=self.proxy_rdns,
                                       proxy_username=self.proxy_username,
                                       proxy_password=self.proxy_password,
                                       socket_options=self.socket_options)


sender = 'ss@ses-china.com'
password = 'Ses123456'
receiver = '1283128015@qq.com'
server = SocksSMTP(
    host='smtp.zmail300.cn',
    port=465,
    proxy_type=socks.SOCKS5,
    proxy_addr='114.106.136.47',
    proxy_port=41362,
)
server.set_debuglevel(1)
server.helo()
content = open('mail.html', 'r', encoding='utf-8').read()
msg = MIMEText(content, 'html', 'utf-8')
msg['Date'] = Header('Date: Fri, 1 Jan 2021 10:46:01 +0800')
msg['From'] = formataddr(('6766.com', sender))
msg['To'] = formataddr(('尊敬的客户', sender))
msg['Subject'] = Header('为什么不显示中文发送者', 'utf-8')
msg['X-Priority'] = Header('3')
msg['X-GUID'] = Header('no')
msg['X-Has-Attach'] = Header('FB69920C-0AC7-411A-8CF5-6A93D5A8FC4D')
msg['X-Mailer'] = Header('Foxmail 7.2.20.259[cn]')
msg['Message-ID'] = Header('<202101011044560629191@ses-china.com>')
server.login(sender, password)
server.sendmail(sender, receiver, msg.as_string())
server.quit()
