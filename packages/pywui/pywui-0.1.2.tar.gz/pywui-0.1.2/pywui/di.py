from typing import Callable, Any


class PyWuiContainer:
    _commands: dict[str, Callable] = {}
    _listeners: dict[str, Callable[[Any], Any]] = {}
    _singleton_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton_instance:
            cls._singleton_instance = super().__new__(cls, *args, **kwargs)
        return cls._singleton_instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._instances = {}

    def get_commands(self):
        return self._commands

    def get_listeners(self):
        return self._listeners

    def register(self, func: Callable, name: str = None):
        command_name = name or func.__name__
        self._commands[command_name] = func

    def listen(self, event: str, func: Callable[[Any], Any]):
        self._listeners[event] = func

    @classmethod
    def instance(cls):
        if cls._singleton_instance is None:
            return cls()
        return cls._singleton_instance
