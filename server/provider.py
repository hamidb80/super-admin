from logging import Logger

from driver.interfaces import TunnelIC
from driver.db import InMemoryDB


class ServicesClass:
    """
    the aim of creating this class is:
    - prevent circular dependency
    - access all necessary objects by import one object
    """

    tunnel: TunnelIC = None

    clientDB: InMemoryDB = None
    messageDB: InMemoryDB = None

    logger: Logger = None


services = ServicesClass()
