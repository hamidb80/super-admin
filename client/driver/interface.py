from typing import Callable, Any, Dict

class TunnelIC:
    event_map: Dict[str, Callable]
    delay: float
    address: str
    is_active: bool

    # add event
    def on(self, event: str, func: Callable):
        pass

    def push_event(self, event: str, data: Any= None):
        pass

    def send(self, event: str, data: Any = None):
        pass

    def get_messages(self):
        pass

    def run(self):
        pass
