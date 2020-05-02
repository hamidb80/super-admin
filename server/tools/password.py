import hashlib
import os

password = None

def hash_password(passwd:str):
    # TODO: encode the password for security
    return passwd

def set_serverpass(passwd: str = None):
    global password

    if passwd is None:
        passwd = input('Enter Server Password \n')

    password = hash_password(passwd)


def check_password(passwd: str) -> bool:
    global password
    return hash_password(passwd) == password
