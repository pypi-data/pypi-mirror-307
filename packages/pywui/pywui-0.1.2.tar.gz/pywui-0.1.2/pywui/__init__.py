from .decorator import command, listener
from .dispatcher import EventDispatcher
from .app import PyWuiApp
from .window import PyWuiWindow

__slots__ = [
    "PyWuiWindow",
    "PyWuiApp",
    "command",
    "listener",
    "EventDispatcher"
]

if __name__ == "__main__":
    app = PyWuiApp("Hello")
    app.run()
