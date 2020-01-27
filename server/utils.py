import hashlib
import os
import codecs

class Password:
    def __init__(self,passwd):
        self.salt = os.urandom(128)
        self.key = hashlib.pbkdf2_hmac('sha256',passwd.encode('utf-8'),self.salt,100000)

