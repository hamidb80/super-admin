from driver.models import Client, Message
from utils import Password_Manager
from provider import services


def connect(client: Client, data=None):
    services.logger.info(f'user {client.host_name} connected')

    services.tunnel.send(target=client.host_name, event='hello', data='hello')


def reconnect(client: Client, data=None):
    pass


def disconnect(client: Client, data=None):
    services.logger.info(f'{client.host_name} disconnected')



# get notifications using this function
def notification(client: Client, data):

    # wrong password notification
    if data['type'] == 'wrongpass':
        services.logger.info(
            f'User {client.host_name} entered a wrong password'
        )

    # access to server notification
    elif data['type'] == 'hasaccess':
        services.logger.info(
            f'User {client.host_name} now has access to server'
        )

    # asking for authentication notification
    elif data['type'] == 'askforauth':
        services.logger.info(
            f'User {client.host_name} asked for running code in server, sending hashed password and salt'
        )

        pass_to_send = Password_Manager.password_list['serverpass']

        client.send(
            'auth',
            {
                'key': str(pass_to_send.key),
                'salt': str(pass_to_send.salt)
            }
        )


# execute command from client with admin privillages
def executefromclient(client: Client, data):
    services.logger.info(f'User {client.host_name} executed command: {data}')

    try:
        exec(data)
    except:
        services.logger.info('Err')
