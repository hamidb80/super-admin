class StateManager:
    def __init__(self):
        self.is_connected = True 
        self.is_admin = False
        self.fails = 0


app_state = StateManager()
