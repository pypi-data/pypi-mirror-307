import contextlib
import json
import ssl
import typing

import aiohttp
import certifi


class SupportsRead[T](typing.Protocol):
    def read(self, __length: int = ...) -> T: ...


ConvertableToBytes: typing.TypeAlias = (
    str
    | bytes
    | bytearray
    | typing.TextIO
    | typing.BinaryIO
    | typing.Iterable['ConvertableToBytes']
)


def get_bytes(x: ConvertableToBytes, encoding: str) -> bytes:
    if isinstance(x, str):
        return x.encode(encoding)
    if isinstance(x, bytes):
        return x
    if isinstance(x, bytearray):
        return bytes(x)
    if (read := getattr(x, 'read', None)) is not None:
        return get_bytes(read(), encoding=encoding)

    if hasattr(x, '__iter__'):
        return b''.join(get_bytes(e, encoding=encoding) for e in iter(x))
    raise RuntimeError('Cannot convert {x} to bytes')


type JsonValue = 'str | int | bool | float | None | JsonArray | JsonObject'
type JsonArray = typing.Sequence[JsonValue]
type JsonObject = typing.Mapping[str, JsonValue]


def json_loads(s: str) -> JsonValue:
    return json.loads(s)


def json_dumps(v: JsonValue):
    return json.dumps(v)


@contextlib.asynccontextmanager
async def make_http_client():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as http_client:
        yield http_client
