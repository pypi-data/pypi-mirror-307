from typing import Callable
from .di import PyWuiContainer

INJECT_WINDOW: str = '__inject__window__'


def command(inject_window: bool = False):
    def decorator(func: Callable):
        PyWuiContainer.instance().register(func)
        setattr(func, INJECT_WINDOW, inject_window)
        return func

    return decorator


def listener(event: str, inject_window: bool = False):
    def decorator(func: Callable):
        setattr(func, INJECT_WINDOW, inject_window)
        PyWuiContainer.instance().listen(event, func)
        return func
    return decorator
