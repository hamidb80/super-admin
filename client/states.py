from driver.core import Core


class StateManager:
    def __init__(self):
        self.is_connected = True
        self.is_admin = False
        self.fails = 0
        self.core: Core = None


app_state = StateManager()
