from typing import Callable, List, Dict
from flask import request
from datetime import datetime

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

    now = datetime.now()
    delta_time = now - client.last_connection

    event = None

    if delta_time.seconds >= client.offline_after:
        event = 'connect'
    else:
        event = 'reconnect'

    services.tunnel.push_event(event, client)

    client.update_connection_time()

    def check(m: Message):
        return m._id > client.last_seen_message_id and m.is_target(client)

    res: List[Message] = services.messageDB.filter(func_checker=check)

    # update client last_seen_message_id
    if len(res):
        msg_ids = [m._id for m in res]
        max_id = max(msg_ids)
        client.last_seen_message_id = max_id

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
