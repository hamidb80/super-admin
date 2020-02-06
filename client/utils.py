import hashlib

from config import APP_NAME

class Password:
    def __init__(self, passwd, salt):

        self.key = hashlib.pbkdf2_hmac(
            'sha256', passwd.encode('utf-8'), salt, 1000000)


class Colors:
    red = '\33[31m'
    green = '\33[32m'
    yellow = '\33[33m'
    blue = '\33[34m'

    bold = '\33[1m'
    italic = '\33[3m'
    end = '\33[0m'


def colored(text: str, styles: str):
    return f'{styles}{text}{Colors.end}'


def cprint(text: str, styles: str):
    return print(colored(text, styles))

class Messages:
    
    connected = colored('Connected', Colors.green)
    
    disconnected = colored('disconnected', Colors.red+Colors.bold)

    you_already_have_admin_priv = colored('You already have admin privillages!', Colors.yellow)

    admin_rights_granted = colored('Admin rights granted', Colors.green)

    wrong_pass = colored('Wrong password!', Colors.red+Colors.bold)

    you_are_connected = colored('You are connected', Colors.green)

    you_arent_connected = colored('You are not connected', Colors.red)
    
    app_name = colored(f'{APP_NAME} >\n', Colors.blue)
    
    running_in_server = colored('You are running commands in server now.', Colors.yellow+Colors.bold)
    
    running_in_client = colored('You are running commands in client now.', Colors.yellow+Colors.bold)
    
    exiting_admin = colored('Exiting admin mode.', Colors.yellow+Colors.bold)
    
    def input(inp):
        return(colored(inp,Colors.yellow+Colors.italic+Colors.bold))