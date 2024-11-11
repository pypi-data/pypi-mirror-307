from .decorator import command, listener, with_app, with_window
from .dispatcher import EventDispatcher
from .app import PyWuiApp
from .window import PyWuiWindow

__slots__ = [
    "PyWuiWindow",
    "PyWuiApp",
    "command",
    "listener",
    "with_window",
    "with_app"
    "EventDispatcher"
]

if __name__ == "__main__":
    app = PyWuiApp("Hello")
    app.run()
