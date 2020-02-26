from typing import Callable, Any, Dict
from abc import abstractmethod


class TunnelIC:
    event_map: Dict[str, Callable]
    delay: float
    address: str
    is_active: bool

    @abstractmethod
    def on(self, event: str, func: Callable):
        pass

    @abstractmethod
    def push_event(self, event: str, data: Any = None):
        pass

    @abstractmethod
    def send(self, event: str, data: Any = None):
        pass

    @abstractmethod
    def get_messages(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def run(self):
        pass
