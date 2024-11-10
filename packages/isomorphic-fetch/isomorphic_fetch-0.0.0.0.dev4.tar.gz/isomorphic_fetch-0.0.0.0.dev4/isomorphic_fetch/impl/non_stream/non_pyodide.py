from collections.abc import Callable
from dataclasses import dataclass

from .common import Response


@dataclass(repr=False)
class Response(Response):
    _content: Callable[[], bytes]
    _text: Callable[[], str]

    @property
    def text(self):
        return self._text()

    @property
    def content(self):
        return self._content()


async def fetch(url: str):
    from niquests import AsyncSession

    async with AsyncSession(happy_eyeballs=True) as session:
        res = await session.get(url)

        assert res.status_code is not None, res

        return Response(res.ok, res.status_code, res.reason, res.headers, lambda: (res.content or b""), lambda: (res.text or ""))
