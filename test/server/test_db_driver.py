from server.driver.db import InMemoryDB
import pytest


class Test:
    @classmethod
    def setup_class(self):
        self.db = InMemoryDB()

    def test_insert(self):
        self.db.add('data')

        assert self.db.data_list == ['data']

    def test_remove(self):
        self.db.add('data')
        self.db.delete(itself='data')

        assert self.db.data_list == []

    def test_get(self):
        self.db.multi_add(['a', 'b', 'b'])

        res = self.db.find(itself='b')

        assert res == 'b'

    def test_filter(self):
        self.db.multi_add(['c', 'c', 'd'])

        res = self.db.filter(itself='c')

        assert res == ['c', 'c']

    def test_func_checker(self):
        self.db.clear()

        self.db.multi_add(['hamid', 'ali', 'reza'])

        res = self.db.filter(lambda name: len(name) > 3)

        assert set(res) == set(('hamid', 'reza'))
