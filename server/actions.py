from server import tunnel

def connect(socket_id, data=None):
    print('a new user connected')

def get_hello(socket_id, data='no data'):
    print(f'user {socket_id} said hello')

def disconnect(socket_id):
    print(f'user {socket_id} gone')