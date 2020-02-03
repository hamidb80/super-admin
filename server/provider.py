from driver.interfaces import TunnelIC
from driver.database import InMemoryDB


class ServicesClass:
    tunnel: TunnelIC
    clientDB: InMemoryDB


services = ServicesClass()
