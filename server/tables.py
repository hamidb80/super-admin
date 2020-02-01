from driver.database import InMemoryDB
from provider import services


def init_database():
    services.clientDB = InMemoryDB()