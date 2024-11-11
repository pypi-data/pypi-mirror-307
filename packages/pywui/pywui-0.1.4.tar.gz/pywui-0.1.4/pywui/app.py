import asyncio
import inspect
import os.path
import platform
import sys
import threading
import typing
from asyncio import AbstractEventLoop
from urllib.parse import urlparse

import ujson
import webview
from ujson import JSONDecodeError
from webview import GUIType, Menu, http, Screen

from .api import PyWuiAPI
from .di import PyWuiContainer
from .dispatcher import EventDispatcher
from .window import PyWuiWindow


class PyWuiApp:

    def __init__(
            self,
            title: str | None = None,
            html: str | None = None,
            width: int = 800,
            height: int = 600,
            x: int | None = None,
            y: int | None = None,
            screen: Screen = None,
            resizable: bool = True,
            fullscreen: bool = False,
            min_size: tuple[int, int] = (200, 100),
            hidden: bool = False,
            frameless: bool = False,
            easy_drag: bool = True,
            shadow: bool = True,
            focus: bool = True,
            minimized: bool = False,
            maximized: bool = False,
            on_top: bool = False,
            confirm_close: bool = False,
            background_color: str = '#FFFFFF',
            transparent: bool = False,
            text_select: bool = False,
            zoomable: bool = False,
            draggable: bool = False,
            vibrancy: bool = False,
            localization: typing.Mapping[str, str] | None = None,
            server: type[http.ServerType] = http.BottleServer,
            http_port: int | None = None,
            server_args: http.ServerArgs = None
    ):
        self.windows: dict[str, PyWuiWindow] = {}
        self.loop: AbstractEventLoop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self._start_event_loop)
        self.webview_params: dict[str, any] = {}
        self.config = self._load_config()
        static: dict[str, any] = self.config.get("static")
        index = self._resource_path(static.get("main"))
        dev_url = static.get("dev_url")
        app_url = index if self._is_frozen else dev_url

        self.window_params: dict[str, any] = self._merge_config({
            "title": title or "PyWui App",
            "url": app_url,
            "html": html,
            "width": width,
            "height": height,
            "x": x,
            "y": y,
            "screen": screen,
            "resizable": resizable,
            "fullscreen": fullscreen,
            "min_size": min_size,
            "hidden": hidden,
            "frameless": frameless,
            "easy_drag": easy_drag,
            "shadow": shadow,
            "focus": focus,
            "minimized": minimized,
            "maximized": maximized,
            "on_top": on_top,
            "confirm_close": confirm_close,
            "background_color": background_color,
            "transparent": transparent,
            "text_select": text_select,
            "zoomable": zoomable,
            "draggable": draggable,
            "vibrancy": vibrancy,
            "localization": localization,
            "server": server,
            "http_port": http_port,
            "server_args": server_args or {},
        }, self.config.get("window", {}))
        self.create_window(
            **self.window_params
        )

    @property
    def _is_frozen(self):
        return hasattr(sys, '_MEIPASS')

    @classmethod
    def _merge_config(cls, dict1, dict2):
        return {key: (dict2.get(key) if key in dict2 and dict2.get(key) is not None else dict1[key]) for key in dict1}

    def _load_config(self) -> dict[str, typing.Any]:
        config_path = self._resource_path('pywui.conf.json')
        if os.path.exists(config_path):
            with open(config_path) as f:
                try:
                    return ujson.load(f)
                except JSONDecodeError:
                    return {}
        return {}

    def _get_icon(self):
        current_os = platform.system().lower()
        icons: dict[str, typing.Any] = self.config.get("icons", {})
        icon = icons.get(current_os, icons.get("linux"))
        return self._resource_path(icon) if icon else None

    def _resource_path(self, relative_path):
        if self._is_frozen:
            return os.path.join(getattr(sys, '_MEIPASS'), relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)

    @classmethod
    def is_url(cls, string):
        parsed = urlparse(string)
        return all([parsed.scheme, parsed.netloc])

    def _start_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _stop_event_loop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.loop_thread.join()

    def get_window(self, key: str) -> PyWuiWindow:
        if key in self.windows:
            return self.windows[key]
        raise KeyError(key)

    def create_window(
            self,
            title: str,
            url: str | None = None,
            html: str | None = None,
            width: int = 800,
            height: int = 600,
            x: int | None = None,
            y: int | None = None,
            screen: Screen = None,
            resizable: bool = True,
            fullscreen: bool = False,
            min_size: tuple[int, int] = (200, 100),
            hidden: bool = False,
            frameless: bool = False,
            easy_drag: bool = True,
            shadow: bool = True,
            focus: bool = True,
            minimized: bool = False,
            maximized: bool = False,
            on_top: bool = False,
            confirm_close: bool = False,
            background_color: str = '#FFFFFFFF',
            transparent: bool = True,
            text_select: bool = False,
            zoomable: bool = False,
            draggable: bool = False,
            vibrancy: bool = False,
            localization: typing.Mapping[str, str] | None = None,
            server: type[http.ServerType] = http.BottleServer,
            http_port: int | None = None,
            server_args: http.ServerArgs = None
    ) -> PyWuiWindow:
        webview_window = webview.create_window(
            title=title,
            url=url,
            html=html,
            js_api=None,
            width=width,
            height=height,
            x=x,
            y=y,
            screen=screen,
            resizable=resizable,
            fullscreen=fullscreen,
            min_size=min_size,
            hidden=hidden,
            frameless=frameless,
            easy_drag=easy_drag,
            shadow=shadow,
            focus=focus,
            minimized=minimized,
            maximized=maximized,
            on_top=on_top,
            confirm_close=confirm_close,
            background_color=background_color,
            transparent=transparent,
            text_select=text_select,
            zoomable=zoomable,
            draggable=draggable,
            vibrancy=vibrancy,
            localization=localization,
            server=server,
            http_port=http_port,
            server_args=server_args or {},
        )
        window = typing.cast(PyWuiWindow, webview_window)
        dispatcher = EventDispatcher(window)
        setattr(window, 'emit', dispatcher.emit)
        setattr(window, 'listen', dispatcher.listen)
        api = PyWuiAPI(app=self, window=window, commands=PyWuiContainer.instance().get_commands())
        window.expose(api.invoke, api.emit)
        self.windows['main' if window.uid == "master" else window.uid] = window

        return window

    def run(
            self,
            func: typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, None] | None] | None = None,
            args: typing.Iterable[typing.Any] | None = None,
            localization: dict[str, str] = None,
            gui: GUIType | None = None,
            debug: bool = False,
            http_server: bool = False,
            http_port: int | None = None,
            user_agent: str | None = None,
            private_mode: bool = True,
            storage_path: str | None = None,
            menu: list[Menu] = None,
            server: type[http.ServerType] = http.BottleServer,
            server_args: dict[typing.Any, typing.Any] = None,
            ssl: bool = False,
            icon: str | None = None
    ):

        def on_start(*s_args, **kwargs):
            if inspect.iscoroutinefunction(func):
                asyncio.run_coroutine_threadsafe(func(*s_args, **kwargs), self.loop)
            else:
                func(*s_args, **kwargs)

        webview_params = {
            'func': on_start,
            'localization': localization or {},
            'gui': gui,
            'args': args if args is not None else [],
            'debug': False if self._is_frozen else debug,
            'http_server': http_server,
            'http_port': http_port,
            'user_agent': user_agent,
            'private_mode': private_mode,
            'storage_path': storage_path,
            'menu': menu or [],
            'server': server,
            'server_args': server_args or {},
            'ssl': ssl,
            'icon': icon or self._get_icon(),
        }
        self.webview_params = webview_params
        self.get_window('main').events.closing += self._stop_event_loop
        self.loop_thread.start()
        if gui == "qt":
            webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False
        webview.start(**webview_params)
