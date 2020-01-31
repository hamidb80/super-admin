from driver.database import InMemoryDB
from states import services


def init_databases():
    services.clientDB = InMemoryDB()