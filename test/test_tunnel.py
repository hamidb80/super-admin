import pytest
from threading import Thread
from time import sleep


from server.driver.tunnel import Tunnel as TunnelServer
from server.config import ADDR, PORT

from client.driver.tunnel import Tunnel as TunnelClient


class TestE2E:
    @classmethod
    def setup_class(self):
        self.server = TunnelServer(ADDR, PORT)
        self.client = TunnelClient(ADDR, PORT)

        self.server_thread = Thread(target=lambda: self.server.run())
        self.client_thread = Thread(target=lambda: self.client.run())

        self.server_thread.start()
        self.client_thread.start()


    def test_run_without_error(self):
        sleep(1)
        assert self.server_thread.is_alive() and self.client_thread.is_alive()

    @classmethod
    def teardown_class(self):
        self.client.stop()
        self.server.stop()
        # TODO: terminate threads after
        pass
