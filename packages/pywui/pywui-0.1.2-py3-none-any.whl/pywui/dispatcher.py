import json
from typing import Any, Callable

from webview import Window

from pywui.di import PyWuiContainer


class EventDispatcher:
    def __init__(self, window: Window):
        self.window = window

    def emit(self, event_name, data=None):
        """Sends an event to JavaScript."""
        payload = json.dumps({"event": event_name, "data": data})
        self.window.evaluate_js(
            f"window.dispatchEvent(new CustomEvent('pywui:{event_name}', {{ detail: {payload} }}));")

    @classmethod
    def listen(cls, event: str, func: Callable[[Any], Any]) -> None:
        PyWuiContainer.instance().listen(event, func)

# Use this dispatcher in main.py after window creation
