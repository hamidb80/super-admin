from states import app_state
from connection import tunnel

def connect():
    app_state.is_connected = True

    # say hello to me and server
    print('hello')
    tunnel.send('hello')


def disconnect():
    app_state.is_connected = False
