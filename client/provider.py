from driver.core import Core
from driver.interface import TunnelIC


class ServicesManager:
    core: Core
    tunnel: TunnelIC

services = ServicesManager()

class StateManager:
    def __init__(self):
        self.host_name: str
        self.is_admin = False
        self.is_connected = False
        self.fails = 0

    def failed_to_connect(self):
        if self.fails > 10 and self.is_connected:
            services.tunnel.push_event('disconnect')
            self.is_connected = False

        self.fails += 1

    def connected_successfully(self):
        if self.is_connected is False:
            self.is_connected = True
            services.tunnel.push_event('connect')

        else:
            services.tunnel.push_event('reconnect')

        self.fails = 0


states = StateManager()
