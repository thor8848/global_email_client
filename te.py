from smtplib import SMTP_SSL, SMTPAuthenticationError, SMTPServerDisconnected, SMTP
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
import requests
import socket
import socks

# xinnet.com	mail exchanger = 20 mx.global-mail.cn.
# xinnet.com	mail exchanger = 20 mx1.global-mail.cn.
# 300.cn	mail exchanger = 50 mx1.zmail300.cn.
# 300.cn	mail exchanger = 1 mxcello.zmail300.cn.
# 300.cn	mail exchanger = 5 mx.zmail300.cn.


sender = 'ss@ses-china.com'
password = 'Ses123456'
receiver = '1283128015@qq.com'

smtp_host = 'smtp.ses-china.com'
server = SMTP_SSL(smtp_host)
# server.proxy_host = '110.18.154.169'
# server.proxy_port = '13869'
server.set_debuglevel(1)
# server.helo()
content = requests.get('http://mail.aliyuncdn.top/demo').text
msg = MIMEText(content, 'html', 'utf-8')
msg['Date'] = Header('Date: Fri, 1 Jan 2021 10:46:01 +0800')
msg['From'] = formataddr(('6766.com', sender))
msg['To'] = formataddr(('尊敬的客户', receiver))
msg['Subject'] = Header('您的专属活动已经上线！', 'utf-8')
msg['X-Priority'] = Header('3')
msg['X-GUID'] = Header('no')
msg['X-Has-Attach'] = Header('FB69920C-0AC7-411A-8CF5-6A93D5A8FC4D')
msg['X-Mailer'] = Header('Foxmail 7.2.20.259[cn]')
msg['Message-ID'] = Header('<202101011044560629191@ses-china.com>')
server.login(sender, password)
server.sendmail(sender, receiver, msg.as_string())
server.quit()
