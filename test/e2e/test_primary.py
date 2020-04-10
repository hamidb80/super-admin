from base import E2ETestBase
from time import sleep


class Test(E2ETestBase):
    def test_connect(self):
        self.push_input('status')

        sleep(1)
        out = self.get_outputs().lower()

        assert 'not connected' not in out and\
            'connected' in out

    def test_auth(self):
        self.push_input('auth')

        sleep(1)
        assert 'password' in self.get_outputs()
