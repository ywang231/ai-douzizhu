# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

# Subscribe event and distribute to listeners

from typing import Optional, Callable
from logger import Logging

__all__ = ['Subscribe', 'Unsubscribe', 'Distribute', 'ClearListeners']


class EventDispatcher:

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(EventDispatcher, cls).__new__(cls)
            Logging("EventDispatcher created")
        return cls.instance

    def __init__(self):  # init would be called each time after new instance created
        if not hasattr(self, 'listeners'):
            self.listeners: dict[str, list] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)

    def notify(self, event_type: str, data: Optional[dict] = None):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)

    def clear_listeners(self):
        self.listeners.clear()


_center = EventDispatcher()

Subscribe = _center.subscribe
Unsubscribe = _center.unsubscribe
Distribute = _center.notify
ClearListeners = _center.clear_listeners


if __name__ == "__main__":
    def listener(data):
        print("Received event data:", data)

    Subscribe("event_type_1", listener)
    Distribute("event_type_1", {"key": "value"})
    Unsubscribe("event_type_1", listener)
    Distribute("event_type_1", {"key": "value"})
