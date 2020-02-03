import hashlib
import os

class Password:
    def __init__(self,passwd):
        
        self.salt = os.urandom(512)
        self.key = hashlib.pbkdf2_hmac('sha256',passwd.encode('utf-8'),self.salt,1000000)


def set_pass():
    
    passwd = input('Enter Server Password \n')
    password = Password(passwd)
    del passwd
    return(password)

