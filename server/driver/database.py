class InMemoryDB:
    def __init__(self, data=[]):
        self.data_list = data

    def add(self, item):
        self.data_list.append(item)

    def delete(self, **indicators):
        res = []

        for item in self.data_list:
            if self._validate(item, indicator) is not True:
                res.append(item)

        self.data_list = res

    def filter(self, **indicators):
        return [
            item for item in self.data_list if self._validate(item, **indicators) is True
        ]

    @staticmethod
    def _validate(item, **indicators):
        for key, val in indicators.items():
            if getattr(item, key) != val:
                return False

        return True

    def find(self, **indicators):
        res = self.filter(**indicators)

        if len(res) is not 0:
            return res[0]

        else:
            return None
