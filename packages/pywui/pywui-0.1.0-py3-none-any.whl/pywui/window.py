from typing import Callable, Any

from webview import Window
from .dispatcher import EventDispatcher


class PyWuiWindow(Window):

    def emit(self, event: str, data: any):
        pass

    def listen(self, event: str, func: Callable[[Any], Any]) -> None:
        pass
