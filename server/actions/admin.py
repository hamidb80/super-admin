from driver.models import Client, Message
from provider import services

from functions import get_online_users
from utils import event_names as ev


def admin_only(action_func):
    def wrapper(c:Client, *args, **kwargs):
        if c.is_admin:
            action_func(c, *args, **kwargs)

    return wrapper

# ---------------------------

@admin_only
def online_users(client: Client, data=None):
    res = get_online_users()

    client.send(ev.online_users_res, res)

@admin_only
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
@admin_only
def execute_from_client(client: Client, data):
    services.logger.info(f'User {client.host_name} executed command: "{data}"')

    try:
        res = str(eval(data))
        client.send(ev.execute_result, res)
    except:
        services.logger.info('Err')
