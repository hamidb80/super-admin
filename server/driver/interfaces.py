from abc import ABC, abstractmethod
from typing import Dict, Callable, Any
from flask import Flask


class TunnelIC:
    event_map: Dict[str, Callable]
    app: Flask

    @abstractmethod
    def __init__(self, addr, port):
        pass

    @abstractmethod
    def on(self, event: str, func: Callable):
        pass

    @abstractmethod
    def push_event(self, event: str, client, data: Any):
        pass

    @abstractmethod
    def send(self, event: str, target: str, data: Any):
        pass

    @abstractmethod
    def run(self):
        pass
