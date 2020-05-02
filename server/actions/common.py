from driver.models import Client, Message
from provider import services

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

    client.send(ev.auth_check, res)
