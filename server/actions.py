from server import tunnel
from config import Password

# variables
clients = {}
clients_inv = {}

# set server's password
passwd = input('Enter Your Password \n')
serverpass = Password(passwd)
del passwd

# functions dependant on events


def connect(socket_id, data=None):
    print(f'user {socket_id} connected')


def disconnect(socket_id):
    print(f'user {clients[socket_id]} disconnected')


def newuser(socket_id, data):

    # add hostname to clients dictionary
    clients[socket_id] = data
    clients_inv = {v: k for k, v in clients.items()}

    # print hostname
    print(f'user {socket_id} is now called {clients[socket_id]}')


def givepass(socket_id):
    tunnel.send('auth', serverpass.key, socket_id)
    print(f'User {clients[socket_id]} asked for running code in server')


def has_access(socket_id):
    print(f'User {clients[socket_id]} now has access to server')


def denied_access(socket_id):
    print(
        f'User {clients[socket_id]} attempted to connect to server but failed'
    )


def execute(socket_id, code):
    print(f'User {clients[socket_id]} executed command {code}')

    try:
        exec(code)
    except:
        print('Err')

# independent functions
