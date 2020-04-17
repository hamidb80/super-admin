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

    event = None

    if client.is_online():
        event = 'reconnect'
    else:
        event = 'connect'

    services.tunnel.push_event(event, client)

    client.update_connection_time()

    def check_unread_messages(m: Message):
        return m._id > client.last_seen_message_id and m.is_target(client)

    res: List[Message]
    res = services.messageDB.filter(func_checker=check_unread_messages)

    # update client last_seen_message_id
    if len(res):
        msg_ids = [m._id for m in res]
        max_id = max(msg_ids)
        client.last_seen_message_id = max_id

    res = [message.jsonify() for message in res]

    return dict(messages=res)


def commit_view(host_name: str):
    client = get_client(host_name)

    data = request.get_json()
    """{
        'event': str,
        'data': any
    }"""

    if client:
        event = data.get('event')
        event_data = data.get('data')

        if event is None:
            return 'event is not defined'

        else:
            services.tunnel.push_event(
                event=event,
                client=client,
                data=event_data
            )
            return 'message committed'

    else:
        return 'access denied'
