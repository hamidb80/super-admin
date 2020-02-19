from typing import Callable, List, Dict
from flask import request

from .models import Client, Message
from provider import services


def get_client(host_name) -> Client:
    return services.clientDB.find(host_name=host_name)


def messages_view(host_name: str):
    client = get_client(host_name)

    m: Message
    res: List[Message] = services.messageDB.filter(lambda m: m.is_target(client))

    res = [message.jsonify() for message in res]

    return dict(messages=res)


def commit_view():
    client_name = request.args.get('client_name')

    client = get_client(client_name)

    if client:
        client.is_admin = True

    if client and client.is_admin:
        target = request.args.get('target')
        event = request.args.get('event')
        data = request.args.get('data')

        new_msg = Message(
            target=target,
            event=event,
            data=data
        )

        new_msg.save()

        return new_msg.jsonify()

    else:
        return 'access denied'


def login_view():
    client_name = request.args.get('client_name')

    if services.clientDB.exists(host_name=client_name):
        return 'dup'

    else:
        new_client = Client(client_name)
        new_client.save()

        return 'hey'
