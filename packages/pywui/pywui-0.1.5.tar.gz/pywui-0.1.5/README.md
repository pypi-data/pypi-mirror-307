<p align="center">

[//]: # (  <a target="_blank"><img src="https://raw.githubusercontent.com/nestipy/nestipy/release-v1/nestipy.png" width="200" alt="Nestipy Logo" /></a></p>)
<p align="center">
    <a href="https://pypi.org/project/pywui">
        <img src="https://img.shields.io/pypi/v/pywui?color=%2334D058&label=pypi%20package" alt="Version">
    </a>
    <a href="https://pypi.org/project/pywui">
        <img src="https://img.shields.io/pypi/pyversions/nestipy.svg?color=%2334D058" alt="Python">
    </a>
    <a href="https://github.com/tsiresymila1/pywui/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/tsiresymila1/pywui" alt="License">
    </a>
</p>

## Description

<p>Pywui is a Python package wrapper for pywebview to make easy the communication between python and JS and async support. </p>

## Getting started

```cmd
    pip install pywui
```

## Exampple

```python
import asyncio
from datetime import datetime

from pywui import command, PyWuiApp, PyWuiWindow, listener


@listener("message", inject_window=True)
async def on_message(window: PyWuiWindow, message: str):
    print("Message received: {}".format(message))


@command(inject_window=True)
async def greet(window: PyWuiWindow):
    # window.toggle_fullscreen()
    window.emit("message", "Hello from python")
    print("Hello :::", window)
    return "Hello World!"


async def on_start(window: PyWuiWindow):
    async def send_time():
        while True:
            window.emit("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            await asyncio.sleep(1)

    await asyncio.create_task(send_time())


app = PyWuiApp(
    "Main Window",
    'http://localhost:5174',
    confirm_close=False
)
main_window = app.get_main_window()
app.run(func=on_start, args=[main_window], debug=True)


```

## Stay in touch

- Author - [Tsiresy Mila](https://tsiresymila.vercel.app)

## License

PyWui is [MIT licensed](LICENSE).
