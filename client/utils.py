import hashlib

class Password:
    def __init__(self,passwd,salt):

        self.key = hashlib.pbkdf2_hmac('sha256',passwd.encode('utf-8'),salt,10000000)


