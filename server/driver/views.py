from typing import Callable, List, Dict
from flask import request

from .models import Client, Message
from provider import services


def get_client(host_name) -> Client:
    client = services.clientDB.find(host_name=host_name)

    if client is None:
        client = Client(host_name)
        client.save()

    return client


def messages_view(host_name: str):
    client = get_client(host_name)
    client.update_connection_time()

    # TODO: delete expaired messages

    def check(m: Message):
        return m.is_target(client)

    res: List[Message] = services.messageDB.filter(func_checker=check)

    res = [message.jsonify() for message in res]

    return dict(messages=res)


def commit_view():
    client_name = request.args.get('client_name')
    client = get_client(client_name)

    if client:
        event = request.args.get('event')
        data = request.args.get('data')

        if event is None:
            return 'event should be defined'

        else:
            services.tunnel.push_event(event, client, data)
            return 'message committed'

    else:
        return 'access denied'
