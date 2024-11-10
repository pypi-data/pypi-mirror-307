from .common import Response


async def fetch(url: str):
    from pyodide.http import pyfetch

    res = await pyfetch(url)

    return Response(res.ok, res.status, res.status_text, res.headers, await res.text())
