from typing import TypedDict, Literal


class ScopeType(TypedDict):
    type: Literal['http', 'lifespan']
    scheme: str
    root_path: str
    server: tuple[str, int]
    http_version: str
    method: str
    path: str
    headers: list[tuple[bytes, bytes]]