from driver.interfaces import TunnelIC
from driver.db import InMemoryDB


class ServicesClass:
    tunnel: TunnelIC
    clientDB: InMemoryDB
    messageDB: InMemoryDB


services = ServicesClass()
