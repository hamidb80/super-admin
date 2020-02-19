from typing import Callable


class InMemoryDB:
    def __init__(self, data: list = None):
        self.data_list = data if data else list()
        self.last_id = 0

    def update_last_id(self):
        self.last_id += 1

    def add(self, item):
        self.data_list.append(item)
        self.update_last_id()

    def delete(self, func_checker: Callable = None, **indicators):
        res = []

        for item in self.data_list:
            if self._validate(item, func_checker=func_checker, **indicators) is not True:
                res.append(item)

        self.data_list = res

    def filter(self, func_checker: Callable = None, **indicators):
        return [
            item for item in self.data_list if self._validate(
                item, func_checker=func_checker, **indicators
            )
        ]

    def exists(self, func_checker: Callable = None, **indicators):
        return bool(self.find(func_checker=func_checker, **indicators))

    def find(self, func_checker: Callable = None, **indicators):
        res = self.filter(func_checker=func_checker, **indicators)

        if len(res) is not 0:
            return res[0]

        else:
            return None

    @staticmethod
    def _validate(item, func_checker: Callable = None, **indicators):
        if func_checker and func_checker(item) is False:
            return False

        for key, val in indicators.items():
            if key == 'equal':
                if item != val:
                    return False
            elif getattr(item, key) != val:
                return False

        return True
