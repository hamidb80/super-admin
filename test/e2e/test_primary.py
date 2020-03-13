from base import E2ETestBase
from time import sleep

class Test(E2ETestBase):
    def test_connect(self):
        self.inp.append('status')

        sleep(1)
        out = self.out_file.get_content().lower()

        assert 'not connected' not in out and\
            'connected' in out

    def test_send_hello(self):
        pass
