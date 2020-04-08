from typing import Callable

class Event:
    """
    event class just for increase readability
    """

    name: str
    function: Callable

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func
