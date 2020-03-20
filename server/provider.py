from driver.interfaces import TunnelIC
from driver.db import InMemoryDB

from logging import Logger


class ServicesClass:
    tunnel: TunnelIC

    clientDB: InMemoryDB
    messageDB: InMemoryDB

    logger: Logger


services = ServicesClass()
