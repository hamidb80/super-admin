from base import E2ETestBase
from time import sleep


class Test(E2ETestBase):
    def test_connect(self):
        self.push_input('status')

        sleep(1)
        out = self.new_outs.lower()

        assert 'not connected' not in out and\
            'connected' in out

    def test_new1(self):
        self.push_input('auth')

        sleep(0.3)
        assert '?' in self.new_outs
