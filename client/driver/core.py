class Core:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode

    def print(self, *args, **kwargs):

        if self.debug_mode:
            pass

        else:
            return print(*args, **kwargs)

    def input(self, text: str):
        if self.debug_mode:
            pass

        else:
            return input(text)
