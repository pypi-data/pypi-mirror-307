import os
import threading
import time
import typing

import webview
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from webview import GUIType, Menu, http, Screen

from .api import PyWuiAPI
from .di import PyWuiContainer
from .dispatcher import EventDispatcher
from .window import PyWuiWindow


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, app: "PyWuiApp"):
        self.app = app

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}. Reloading window...")
            self.app.restart()


class PyWuiApp:

    def __init__(
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
        self._observer: Observer = None
        self.webview_params = {}
        self.window_params = {
            "title": title,
            "url": url,
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
        }
        self._main_window = self.create_window(
            **self.window_params
        )
        self.should_reload = False

    def get_main_window(self) -> PyWuiWindow:
        return self._main_window

    @classmethod
    def create_window(
            cls,
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
        api = PyWuiAPI(window=window, commands=PyWuiContainer.instance().get_commands())
        window.expose(api.invoke, api.emit)

        return window

    def start_file_watcher(self):
        # Start a watchdog observer to monitor for file changes
        event_handler = ReloadHandler(self)
        self._observer = Observer()
        self._observer.schedule(event_handler, path=os.getcwd(), recursive=True)
        self._observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._observer.stop()
        self._observer.join()

    def restart(self):
        if self._observer:
            self._observer.stop()
            # self._observer.join()
        self._main_window.destroy()
        print("Restarted")
        self._main_window = self.create_window(**self.window_params)
        if threading.current_thread() is threading.main_thread():
            webview.start(**self.webview_params)
        else:
            threading.Thread(target=self.restart, daemon=True).start()

    def run(self,
            on_start: typing.Callable[..., None] | None = None,
            on_start_args: typing.Iterable[typing.Any] | None = None,
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
        webview_params = {
            'func': on_start,
            'localization': localization or {},
            'gui': gui,
            'args': on_start_args if on_start_args is not None else [],
            'debug': debug,
            'http_server': http_server,
            'http_port': http_port,
            'user_agent': user_agent,
            'private_mode': private_mode,
            'storage_path': storage_path,
            'menu': menu or [],
            'server': server,
            'server_args': server_args or {},
            'ssl': ssl,
            'icon': icon,
        }
        self.webview_params = webview_params
        # if debug:
        #     threading.Thread(target=self.start_file_watcher, daemon=True).start()
        webview.start(**webview_params)
