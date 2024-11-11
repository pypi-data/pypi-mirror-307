import asyncio
import inspect
import traceback
import typing
from typing import Callable

from .decorator import INJECT_WINDOW, INJECT_APP
from .di import PyWuiContainer
from .window import PyWuiWindow

if typing.TYPE_CHECKING:
    from .app import PyWuiApp


class PyWuiAPI:
    window: PyWuiWindow = None

    def __init__(self, app: "PyWuiApp", window: PyWuiWindow, commands: dict[str, Callable]):
        self.commands: dict[str, Callable] = commands
        self.app = app
        self.window = window

    def execute_function(self, func: Callable, *args, **kwargs):
        if inspect.iscoroutinefunction(func):
            future = asyncio.run_coroutine_threadsafe(func(*args, **kwargs), self.app.loop)
            return future.result()
        else:
            return func(*args, **kwargs)

    def emit(self, event: str, *args, **kwargs):
        listeners = PyWuiContainer.instance().get_listeners()
        if event in listeners:
            listener = listeners[event]
            app = getattr(listener, INJECT_APP, False)
            win = getattr(listener, INJECT_WINDOW, False)
            inject_args: list = []
            if app:
                inject_args.append(self.app)
            if win:
                inject_args.append(self.window)
            self.execute_function(listener, *inject_args, *args, **kwargs)

    def invoke(self, command_name: str, *args, **kwargs):
        """Executes a registered command and returns the result as JSON."""
        if command_name in self.commands:
            try:
                command = self.commands[command_name]
                inject = getattr(command, INJECT_WINDOW, False)
                if inject:
                    result = self.execute_function(command, self.window, *args, **kwargs)
                else:
                    result = self.execute_function(command, *args, **kwargs)
                return {"status": "success", "data": result}
            except Exception as exception:
                tb_list = traceback.extract_tb(exception.__traceback__)
                e = {
                    'type': type(exception).__name__,
                    'message': str(exception),
                    'traceback': [
                        {
                            "file": frame.filename,
                            "line": frame.lineno,
                            "function": frame.name,
                            "code": frame.line
                        }
                        for frame in tb_list
                    ],
                }
                return {"status": "error", "message": e}
        return {"status": "error", "message": f"Command {command_name} not found"}
