from server import tunnel

# variables

clients = {}
clients_inv = {}

# functions dependant on events


def connect(socket_id, data=None):
    print(f'user {socket_id} connected')


def disconnect(socket_id):
    print(f'user {clients[socket_id]} disconnected')


def newname(socket_id, data):
    clients[socket_id] = data
    clients_inv = {v: k for k, v in clients.items()}

    print(f'user {socket_id} is now called {clients[socket_id]}')


def execute(socket_id, code):
    print(f'User {clients[socket_id]} executed command {code}')

    try:
        exec(code)
    except:
        print('Err')
