from collections.abc import Mapping
from dataclasses import dataclass
from functools import cached_property
from http import HTTPStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..common import AbstractResponse
else:
    AbstractResponse = object


@dataclass(repr=False)
class Response(AbstractResponse):
    ok: bool
    status: int
    phrase: str | None
    headers: Mapping[str, str]

    if TYPE_CHECKING:
        content = property(lambda _: b"")
        text = property(lambda _: "")

    @property
    def status_text(self):
        return self.phrase or HTTPStatus(self.status).phrase

    @cached_property
    def json(self):
        from json import loads

        return loads(self.content)

    def __repr__(self):
        return f"<Response {self.status}>"
