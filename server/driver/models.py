# from server import tunnel
from tables import clients_manager

class Client:
    db = clients_manager

    def __init__(self, socket_id: str):
        self.socket_id = socket_id
        self.host_name = None

    @property
    def is_unknown(self):
        return self.host_name is None

    # def send(self, event: str, data=None):
    #     tunnel.send(event, data, socket_id=self.socket_id)

    def disconnect(self):
        pass

    # save this client to db
    def save(self):
        self.db.add(self)

    # delete this client from db
    def delete(self):
        self.db.delete(socket_id=self.socket_id)

