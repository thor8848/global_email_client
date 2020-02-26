# -*-coding:utf-8-*-
from smtplib import SMTP_SSL, SMTPAuthenticationError
from mylib.code_logging import Logger as Log
from requests.exceptions import RequestException
from email.mime.text import MIMEText
from mylib.tools import encode_header
from email.header import Header
import requests
import time
import random
import uuid

log = Log('send_email.log').get_log()


def get_email_mission():
    response = requests.get('http://139.196.96.86:5004/email/', timeout=2)
    return response.json()


def get_global_account():
    response = requests.get('http://139.196.96.86:5004/account/')
    return response.json()


def send_mail_mission():
    ...


if __name__ == '__main__':
    rand_time = random.randint(10, 20)
    log.warning('RANDOM WAIT {}'.format(rand_time))
    time.sleep(rand_time)
    while True:
        mission_data = dict()
        try:
            log.warning('CONNECT EMAIL SERVER')
            mission_data = get_email_mission()
            while True:
                account_data = get_global_account()
                username = account_data['username']
                password = account_data['password']
                try:
                    smtp_host = 'smtp.global-mail.cn'
                    log.warning('ACCOUNT LOGIN TRY {} {}'.format(username, password))
                    server = SMTP_SSL(smtp_host)
                    # server.set_debuglevel(1)
                    server.ehlo(smtp_host)
                    server.login(username, password)
                    break
                except SMTPAuthenticationError:
                    log.warning('ACCOUNT FAILED {}{}'.format(username, password))
                    continue
            message = MIMEText(mission_data['message'], _subtype='html', _charset='utf-8')
            message['Accept-Language'] = "zh-CN"
            message['Accept-Charset'] = "ISO-8859-1,UTF-8"
            message['From'] = encode_header(mission_data['from'], username)
            message['To'] = encode_header(mission_data['to'], '')
            message['Message-ID'] = uuid.uuid4().__str__()
            message['Subject'] = Header(mission_data['subject'], 'utf-8')
            message['MIME-Version'] = '1.0'
            server.sendmail(username, mission_data['receivers'], message.as_string())
            log.debug('SEND SUCCESS EMAIL')
            log.warning('WAITING {} SEC'.format(mission_data['delay']))
            time.sleep(int(mission_data['delay']))
        except RequestException:
            log.warning('CONNECT FAIL RETRY')
            time.sleep(10)
