from server.driver.database import InMemoryDB
import pytest


class TestE2E:
    @classmethod
    def setup_class(self):
        self.db = InMemoryDB()

    def test_insert(self):
        self.db.add('data')

        assert self.db.data_list == ['data']

    def test_remove(self):
        self.db.add('data')
        self.db.delete(equal='data')

        assert self.db.data_list == []

    def test_get(self):
        self.db.add('b')
        self.db.add('b')
        self.db.add('a')

        res = self.db.find(equal='b')

        assert res == 'b'

    def test_filter(self):
        self.db.add('c')
        self.db.add('c')
        self.db.add('d')

        res = self.db.filter(equal='c')

        assert res == ['c', 'c']
