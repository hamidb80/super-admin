class InMemoryDB:
    def __init__(self, data=[]):
        self.data_list = data

    def add(self, item):
        self.data_list.append(item)

    def delete(self, **indicator):
        res = []

        for item in self.data_list:
            if self._has_conditions(item, indicator) is not True:
                res.append(item)

        self.data_list = res

    def filter(self, **indicator):
        return [
            item for item in self.data_list if self._has_conditions(item, **indicator) is True
        ]

    @staticmethod
    def _has_conditions(item, **indicator):
        for key, val in indicator.items():
            if getattr(item, key) != val:
                return False

        return True

    def find(self, **indicator):
        res = self.filter(**indicator)

        if len(res) is not 0:
            return res[0]

        else:
            return None
