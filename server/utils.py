import hashlib
import os


class Password:
    def __init__(self, passwd):

        self.salt = os.urandom(512)
        self.key = hashlib.pbkdf2_hmac(
            'sha256', passwd.encode('utf-8'), self.salt, 1000000)


def set_serverpass(passwd: str = None):

    if passwd is None:
        passwd = input('Enter Server Password \n')

    Password_Manager.password_list['serverpass'] = Password(passwd)


class Password_Manager:
    password_list = {}
