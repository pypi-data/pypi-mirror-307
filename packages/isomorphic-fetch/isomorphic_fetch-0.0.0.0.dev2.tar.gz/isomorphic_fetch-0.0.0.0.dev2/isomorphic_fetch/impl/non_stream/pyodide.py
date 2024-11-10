from .common import Response


async def fetch(url: str):
    from pyodide.http import pyfetch

    res = await pyfetch(url)

    return Response(res.ok, res.status, res.headers, await res.text())
