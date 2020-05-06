import os
from time import sleep
from socket import gethostname

from base import E2ETestBase


class Test(E2ETestBase):

    @classmethod
    def init(self):
        self.login()

    @classmethod
    def destroy(self):
        self.push_input(self, 'quit')
        self.wait(self)

    @classmethod
    def login(self):
        password = os.getenv('server_pass')

        self.push_input(self, 'auth')
        self.wait(self)

        self.push_input(self, password)

        self.wait(self)

    # tests ---------------------------

    def test_run_command_in_server(self):
        # run code in the server
        self.push_input('exec 7 * 7')
        self.wait()

        assert '49' in self.get_outputs().lower()

    def test_get_online_clients(self):
        my_host_name = gethostname()

        self.push_input('get online-users')
        self.wait()

        out = self.get_outputs().lower()

        assert my_host_name in out


    def test_push_event_without_data(self):
        self.push_input('send hello')
        self.wait()

        out = self.get_outputs().lower()

        assert 'server said hello' in out

    # TODO: push event also with data