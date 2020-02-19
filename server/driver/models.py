from provider import services
from .db import InMemoryDB
from typing import Any
from abc import abstractproperty, abstractmethod


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

        super().__init__()

    @property
    def db(self) -> InMemoryDB:
        return services.clientDB

    def send(self, event: str, data=None):
        new_msg = Message(target=self.host_name, event=event, data=data)
        services.tunnel.send(new_msg)


class Message(Model):
    def __init__(self, target: str, event: str, data: Any):
        self.target = target  # can be 'all', 'admin, '<client.host_name>
        self.event = event
        self.data = data

        super().__init__()

    @property
    def db(self) -> InMemoryDB:
        return services.messageDB

    def jsonify(self):
        return dict(target=self.target, event=self.event, data=self.data,
                    id=self._id)

    def is_target(self, client: Client):
        if self.target == 'admin':
            return client.is_admin

        elif self.target == 'all':
            return True

        return self.target == client.host_name
