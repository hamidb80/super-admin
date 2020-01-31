from states import services
from .database import InMemoryDB


class Client:
    def __init__(self, socket_id: str):
        self.socket_id = socket_id
        self.host_name = None

    @property
    def db(self) -> InMemoryDB:
        return services.clientDB

    @property
    def is_unknown(self):
        return self.host_name is None

    def name_or_id(self):
        return self.socket_id if self.is_unknown else self.host_name

    def send(self, event: str, data=None):
        services.tunnel.send(event, data, socket_id=self.socket_id)

    def disconnect(self):
        pass

    # save this client to db
    def save(self):
        self.db.add(self)

    # delete this client from db
    def delete(self):
        self.db.delete(socket_id=self.socket_id)
