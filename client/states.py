class StateManager:
    def __init__(self):
        self.is_connected = False
        self.is_admin = False
        self.main_input_is_waiting = True
        self.client_is_waiting = True


app_state = StateManager()
