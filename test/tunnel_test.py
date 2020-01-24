import pytest
from threading import Thread
from time import sleep


from server.driver.tunnel import Tunnel as TunnelServer
from server.config import ADDR, PORT

from client.driver.tunnel import Tunnel as TunnelClient


class TestServer:
    def test_run_without_error(self):
        server = TunnelServer(ADDR, PORT)
        client = TunnelClient(ADDR, PORT)

        server_thread = Thread(target=lambda: server.run())
        client_thread = Thread(target=lambda: client.run())

        server_thread.start()
        client_thread.start()


        sleep(1)

        assert server_thread.is_alive() and client_thread.is_alive()
