from driver.models import Client, Message
from utils import Password_Manager
from provider import services


def connect(client: Client, data=None):
    print(f'user {client.host_name} connected')

    services.tunnel.send(target=client.host_name, event='hello', data= 'hello')

def reconnect(client:Client, data=None):
    pass


# get notifications using this function
def notification(client: Client, data):

    # wrong password notification
    if data['type'] == 'wrongpass':
        print(f'User {client.host_name} entered a wrong password')

    # access to server notification
    elif data['type'] == 'hasaccess':
        print(f'User {client.host_name} now has access to server')

    # asking for authentication notification
    elif data['type'] == 'askforauth':

        print(
            f'User {client.host_name} asked for running code in server, sending hashed password and salt.')

        pass_to_send = Password_Manager.password_list['serverpass']

        client.send('auth', {'key': pass_to_send.key,
                             'salt': pass_to_send.salt})


# execute command from client with admin privillages
def executefromclient(client: Client, data):
    print(f'User {client.host_name} executed command: {data}')

    try:
        exec(data)
    except:
        print('Err')
