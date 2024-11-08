import traceback
from typing import Callable

from .decorator import INJECT_WINDOW
from .di import PyWuiContainer
from .window import PyWuiWindow


class PyWuiAPI:
    window: PyWuiWindow = None

    def __init__(self, window: PyWuiWindow, commands: dict[str, Callable]):
        self.commands: dict[str, Callable] = commands
        self.window = window

    def emit(self, event: str, *args, **kwargs):
        listeners = PyWuiContainer.instance().get_listeners()
        if event in listeners:
            listener = listeners[event]
            inject = getattr(listener, INJECT_WINDOW, False)
            if inject:
                listener(self.window, *args, **kwargs)
            else:
                listener(*args, **kwargs)

    def invoke(self, command_name: str, *args, **kwargs):
        """Executes a registered command and returns the result as JSON."""
        if command_name in self.commands:
            try:
                command = self.commands[command_name]
                inject = getattr(command, INJECT_WINDOW, False)
                print(self.window, *args, **kwargs)
                if inject:
                    result = command(self.window, *args, **kwargs)
                else:
                    result = command(*args, **kwargs)

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
