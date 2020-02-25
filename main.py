# -*-coding:utf-8-*-
from smtplib import SMTP_SSL, SMTPAuthenticationError
from mylib.code_logging import Logger as Log
from requests.exceptions import RequestException
import requests
import time

log = Log('send_email.log').get_log()


def get_email_mission():
    response = requests.get('http://139.196.96.86:5004/email/', timeout=2)
    return response.json()


def get_global_account():
    response = requests.get('http://139.196.96.86:5004/account/')
    return response.json()


def send_mail_mission():
    mission_data = get_email_mission()
    while True:
        try:
            account_data = get_global_account()
            username = account_data['username']
            password = account_data['password']
            smtp_host = 'smtp.global-mail.cn'
            log.warning(f'ACCOUNT LOGIN TRY {username}{password}')
            server = SMTP_SSL(smtp_host)
            server.set_debuglevel(1)
            server.ehlo(smtp_host)
            server.login(username, password)
            break
        except SMTPAuthenticationError:
            log.warning(f'ACCOUNT FAILED {username}{password}')
            continue
    server.sendmail(username, mission_data['receivers'], mission_data['message'])
    log.debug(f'SEND SUCCESS EMAIL')


if __name__ == '__main__':
    while True:
        try:
            send_mail_mission()
            time.sleep(120)
        except RequestException:
            time.sleep(120)
