from typing import List

from provider import services
from driver.models import Message, Client

from utils import event_names as ev

# -----------------------------------------------------------
def check_is_expaired(m: Message):
    return m.is_expaired()


def clean_messageDB():
    services.messageDB.delete(func_checker=check_is_expaired)


# -----------------------------------------------------------
offline_clients = set()


def is_offline(c: Client):
    return c.is_online() is False


def remove_from_offline_clients(client: Client, data=None):
    global offline_clients

    if client.host_name in offline_clients:
        offline_clients.remove(client.host_name)


def check_for_disconnection():
    global offline_clients

    clients = services.clientDB.filter(func_checker=is_offline)

    client: Client
    for client in clients:
        if client.host_name not in offline_clients:
            services.tunnel.push_event(ev.disconnect, client)
            offline_clients.add(client.host_name)


def get_online_users() -> List[str]:
    c: Client

    res = services.clientDB.filter(lambda c: c.is_online())
    res = [c.host_name for c in res]

    return res
