from collections.abc import Mapping


class AbstractResponse:
    headers: Mapping[str, str]
    status: int
    ok: bool
