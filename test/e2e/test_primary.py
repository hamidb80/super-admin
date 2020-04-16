from base import E2ETestBase
from time import sleep

import os


class Test(E2ETestBase):
    def test_connect(self):
        self.push_input('status')

        self.wait()

        out = self.get_outputs().lower()

        assert 'not connected' not in out and\
            'connected' in out

    def test_auth(self):
        correct_pass = os.getenv('server_pass')
        wrong_pass = '46164'

        # check auth commnad works

        self.push_input('auth')
        self.wait()

        assert 'password' in self.get_outputs().lower()

        # wrong password enter check

        self.push_input(wrong_pass)
        self.wait()

        assert 'wrong' in self.get_outputs().lower()

        # correct password enter check

        self.push_input(correct_pass)
        self.wait()

        assert 'admin' in self.get_outputs().lower()

        self.push_input('exit')
        self.wait()

    def test_help(self):
        self.push_input('help')
        self.wait()

        out = self.get_outputs().lower()

        assert 'command' in out