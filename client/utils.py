import hashlib

class Password:
    def __init__(self,passwd,salt):

        self.key = hashlib.pbkdf2_hmac('sha256',passwd.encode('utf-8'),salt,1000000)


class Colors:
    red      = '\33[31m'
    green    = '\33[32m'
    yellow   = '\33[33m'
    blue     = '\33[34m'
    
    bold     = '\33[1m'
    italic   = '\33[3m'
    end      = '\33[0m'