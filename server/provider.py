from driver.interfaces import TunnelIC
from driver.db import InMemoryDB

from logging import Logger


class ServicesClass:
    tunnel: TunnelIC = None

    clientDB: InMemoryDB = None
    messageDB: InMemoryDB = None

    logger: Logger = None


services = ServicesClass()
