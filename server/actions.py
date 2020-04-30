from driver.models import Client, Message
from provider import services

from functions import get_online_users
from tools.password import check_password
from utils import event_names as ev


def connect(client: Client, data=None):
    services.logger.info(f'user {client.host_name} connected')

    services.tunnel.send(target=client.host_name, event='hello', data='hello')


def reconnect(client: Client, data=None):
    pass


def disconnect(client: Client, data=None):
    services.logger.info(f'{client.host_name} disconnected')


def auth(client: Client, entered_pass: str):
    res = check_password(entered_pass)

    if res:
        client.is_admin = True

    client.send('auth_check', res)


def online_users(client: Client, data=None):
    res = get_online_users()

    client.send(ev.online_users_res, res)


def send_event(client: Client, data: dict):
    """
    data: {
        'event': str
        'data': str
    }
    """

    services.tunnel.send(
        event=data['event'], data=data['data'],
        target='all',
    )

# execute command from client with admin privillages


def execute_from_client(client: Client, data):
    services.logger.info(f'User {client.host_name} executed command: "{data}"')

    try:
        res = str(eval(data))
        client.send(ev.execute_result, res)
    except:
        services.logger.info('Err')
