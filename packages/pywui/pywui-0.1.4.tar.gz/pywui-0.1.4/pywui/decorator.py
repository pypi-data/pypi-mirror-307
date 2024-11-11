from typing import Callable, Union
from .di import PyWuiContainer

INJECT_APP: str = '__inject__window__'
INJECT_WINDOW: str = '__inject__app__'


def with_app(func: Callable) -> Callable:
    setattr(func, INJECT_APP, True)
    return func


def with_window(func: Callable) -> Callable:
    setattr(func, INJECT_WINDOW, True)
    return func


def command(name: Union[str, None] = None):
    def decorator(func: Callable):
        PyWuiContainer.instance().register(func, name)
        return func

    return decorator


def listener(event: str):
    def decorator(func: Callable):
        PyWuiContainer.instance().listen(event, func)
        return func

    return decorator
