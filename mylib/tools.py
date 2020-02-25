import requests
from random import choice, sample
import base64


def encode_header(string, email):
    s = string.encode('utf-8')
    return f'=?UTF-8?B?{str(base64.b64encode(s), encoding="utf-8")}?= <{email}>'


def local_ip():
    response = requests.get('http://icanhazip.com/')
    ip = response.text.strip()
    return ip


def rand_from():
    file = open('content/from.txt', 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    return choice(data)


def rand_to():
    file = open('content/to.txt', 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    return choice(data)


def rand_title():
    file = open('content/title_1.txt', 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    return choice(data)


def rand_chars():
    string = "qwertyuiopasdfghjklzxcvbnm"
    return ''.join(sample(string, 5))


def rand_account():
    file = open('account/user.txt', 'r', encoding='utf-8')
    data = []
    for line in file:
        data.append(line.strip())
    string = str(choice(data)).split(' ')
    return string[0], string[1].strip()

