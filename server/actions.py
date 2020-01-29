from server import tunnel
from utils import Password

## variables

clients = {}
clients_inv = {}

# set server's password
passwd = input('Enter Server Password \n')
serverpass = Password(passwd)
del passwd

## functions dependant on events

def connect(socket_id, data=None):
    # user connection notification
    print(f'user {socket_id} connected')


def disconnect(socket_id, data=None):
    # user connection notification
    print(f'user {clients[socket_id]} disconnected')

# get notifications using this function
def notification(socket_id,data):
    
    # new user notification
    if data['type']=='connection_initials':
        # change clients and clients_inv globally
        global clients, clients_inv
        
        # make dictionaries of clients connected to server
        clients[socket_id] = data['hostname']
        clients_inv = {v: k for k, v in clients.items()}
        
        # anounce new name 
        print(f'User {socket_id} is now called {clients[socket_id]}')
        
    # wrong password notification
    elif data['type']=='wrongpass':
        print(f'User {clients[socket_id]} entered a wrong password')
    
    # illegal command notification    
    elif data['type']=='illegalcommand':
        print(f'User {clients[socket_id]} attempted to run an illegal command')

    # access to server notification
    elif data['type']=='hasaccess':
        print(f'User {clients[socket_id]} now has access to server')
    
    # asking for authentication notification
    elif data['type']=='askforauth':    
        print(f'User {clients[socket_id]} asked for running code in server, sending hashed password and salt.')
        tunnel.send('auth',{'key': serverpass.key, 'salt': serverpass.salt}, socket_id)
        
        
# execute command from client with admin privilages
def executefromclient(socket_id, data):
    print(f'User {clients[socket_id]} executed command: {data}')

    try:
        exec(data)
    except:
        print('Err')

## independent functions
