from base import E2ETestBase
from time import sleep

import os
from socket import gethostname


class Test(E2ETestBase):

    @classmethod
    def init(self):
        self.login()

    @classmethod
    def destroy(self):
        self.push_input(self, 'exit')
        self.wait(self)

    @classmethod
    def login(self):
        password = os.getenv('server_pass')

        self.push_input(self, 'auth')
        self.wait(self)

        self.push_input(self, password)

        self.wait(self)

    def test_get_online_clients(self):
        my_host_name = gethostname()

        self.push_input('online-users')
        self.wait()

        out = self.get_outputs().lower()

        assert my_host_name in out
