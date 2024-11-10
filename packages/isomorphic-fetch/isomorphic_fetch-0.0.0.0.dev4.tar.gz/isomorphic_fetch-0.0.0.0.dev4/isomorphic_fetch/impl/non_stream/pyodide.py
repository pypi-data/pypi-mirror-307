from dataclasses import dataclass

from pyodide.ffi import JsBuffer

from .common import Response


@dataclass(repr=False)
class Response(Response):
    _buffer: JsBuffer

    @property
    def text(self):
        return self._buffer.to_string()

    @property
    def content(self):
        return self._buffer.to_bytes()


async def fetch(url: str):
    from pyodide.http import pyfetch

    res = await pyfetch(url)

    return Response(res.ok, res.status, res.status_text, res.headers, await res.buffer())
