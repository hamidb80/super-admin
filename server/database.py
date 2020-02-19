from driver.db import InMemoryDB
from provider import services


def init_database():
    services.clientDB = InMemoryDB()
    services.messageDB = InMemoryDB()