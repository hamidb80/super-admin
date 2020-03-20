from abc import abstractproperty, abstractmethod
from typing import Any
from datetime import datetime, timedelta

from provider import services
from config import CLIENT_IS_OFFLINE_AFTER, MESSAGE_EXPIRE_TIME
from .db import InMemoryDB


class Model:
    _id: int

    def __init__(self):
        self._id = self.db.last_id

    @abstractproperty
    def db(self) -> InMemoryDB:
        pass

    # save this client to db
    def save(self):
        self.db.add(self)

    def delete(self):
        self.db.delete(_id=self._id)


class Client(Model):

    def __init__(self, host_name: str):
        self.host_name = host_name
        self.is_admin = False
        self.last_connection = datetime.now()
        self.last_seen_message_id = -1

        super().__init__()

    @property
    def db(self) -> InMemoryDB:
        return services.clientDB

    def update_connection_time(self):
        self.last_connection = datetime.now()

    def is_online(self) -> bool:
        delta_time: timedelta = datetime.now() - self.last_connection
        return delta_time.seconds <= CLIENT_IS_OFFLINE_AFTER

    def send(self, event: str, data=None):
        services.tunnel.send(target=self.host_name, event=event, data=data)


class Message(Model):
    def __init__(self, target: str, event: str, data: Any):
        self.target = target  # can be 'all', 'admin, '<client.host_name>
        self.event = event
        self.data = data
        self.time: datetime = None

        super().__init__()

    @property
    def db(self) -> InMemoryDB:
        return services.messageDB

    def is_expaired(self) -> bool:
        delta_time: timedelta = datetime.now() - self.time

        return delta_time.seconds > MESSAGE_EXPIRE_TIME

    def save(self):
        self.time = datetime.now()

        super().save()

    def jsonify(self):
        return dict(event=self.event, data=self.data)

    def __repr__(self):
        return f"event {self.event} for {self.target}"

    def is_target(self, client: Client):
        if self.target == 'admin':
            return client.is_admin

        elif self.target == 'all':
            return True

        return self.target == client.host_name
