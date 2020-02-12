import hashlib

from config import APP_NAME

class Password:
    def __init__(self, passwd, salt):

        self.key = hashlib.pbkdf2_hmac(
            'sha256', passwd.encode('utf-8'), salt, 1000000)


class Messages:
    
    connected = 'Connected'
    
    disconnected = 'disconnected'

    eror = 'Err'

    you_already_have_admin_priv = 'You already have admin privillages!'

    admin_rights_granted = 'Admin rights granted'

    wrong_pass = 'Wrong password!'

    you_are_connected = 'You are connected'

    you_arent_connected = 'You are not connected'
    
    app_name = f'{APP_NAME} >\n'
    
    running_in_server = 'You are running commands in server now.'
    
    running_in_client = 'You are running commands in client now.'
    
    exiting_admin = 'Exiting admin mode.'

    enter_pass = "Enter server's password >\n"