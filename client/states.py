class StateManager:
    def __init__(self):
        self.is_connected = False
        self.is_admin = False
        self.is_waiting = False


app_state = StateManager()
