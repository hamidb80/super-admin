from provider import services
from .db import InMemoryDB
from typing import Any
from abc import abstractproperty, abstractmethod

from datetime import datetime, timedelta


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
    # per secs
    offline_after = 1

    def __init__(self, host_name: str):
        self.host_name = host_name
        self.is_admin = False
        self.last_connection = datetime.now()

        super().__init__()

    @property
    def db(self) -> InMemoryDB:
        return services.clientDB

    def update_connection_time(self):
        self.last_connection = datetime.now()

    def is_online(self):
        delta_time: timedelta = datetime.now() - self.last_connection
        return delta_time.seconds < self.offline_after

    def send(self, event: str, data=None):
        new_msg = Message(target=self.host_name, event=event, data=data)
        services.tunnel.send(new_msg)


class Message(Model):
    # per secs
    expaired_after = 5

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

        return delta_time.seconds > self.expaired_after

    def save(self):
        self.time = datetime.now()

        super().save()

    def jsonify(self):
        return dict(target=self.target, event=self.event, data=self.data,
                    id=self._id)

    def is_target(self, client: Client):
        if self.target == 'admin':
            return client.is_admin

        elif self.target == 'all':
            return True

        return self.target == client.host_name
