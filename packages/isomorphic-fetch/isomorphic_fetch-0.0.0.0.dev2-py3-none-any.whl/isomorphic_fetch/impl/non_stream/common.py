from collections.abc import Mapping
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..common import AbstractResponse
else:
    AbstractResponse = object


class Response(AbstractResponse):
    def __init__(self, ok: bool, status: int, headers: Mapping[str, str], text: str):
        self.ok = ok
        self.status = status
        self.headers = headers
        self.text = text

    @cached_property
    def json(self):
        from json import loads

        return loads(self.text)

    def __repr__(self):
        return f"<Response {self.status}>"
