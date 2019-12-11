from driver.tunnel import Tunnel
from config import ADDR, PORT

tunnel = Tunnel(ADDR, PORT)

def connection(socket_id, data=None):
    print('a new user connected')

def get_hello(socket_id, data='no data'):
    print(f'user {socket_id} said hello')

tunnel.on('connect', connection)
tunnel.on('hello', get_hello)
# tunnel.on('disconnect', )

tunnel.listen()