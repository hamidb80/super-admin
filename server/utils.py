import hashlib

class Password:
    def __init__(self,passwd):

        self.key = hashlib.pbkdf2_hmac('sha256',passwd.encode('utf-8'),
        b'\n\x91FP\xb4\xae~\x04\xce(\xfe\x8b\x91\x97w.\xb3Di\x001\x15\xc5;\x92BLz\xdcc\xdb\x18'
        ,100000
        )
