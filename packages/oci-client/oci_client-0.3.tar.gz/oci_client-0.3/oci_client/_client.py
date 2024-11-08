import base64
import contextlib
import dataclasses
import email.utils
import enum
import functools
import hashlib
import typing
import urllib.parse

import aiohttp
import pydantic
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.types import rsa
from cryptography.hazmat.primitives.hashes import SHA256

from oci_client import _helpers, _services, cfg


class HttpMethod(enum.Enum):
    CONNECT = enum.auto()
    DELETE = enum.auto()
    GET = enum.auto()
    HEAD = enum.auto()
    OPTIONS = enum.auto()
    PATCH = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    TRACE = enum.auto()

    @property
    def has_body(self):
        return self in {HttpMethod.POST, HttpMethod.PUT, HttpMethod.PATCH}


class ContentType(enum.Enum):
    JSON = enum.auto()
    OCTET_STREAM = enum.auto()


@dataclasses.dataclass
class Request:
    method: HttpMethod
    url: urllib.parse.ParseResult
    content: bytes
    content_type: ContentType


@dataclasses.dataclass
class Response:
    status_code: int
    content: bytes
    headers: dict[str, str]

    @functools.cached_property
    def text(self) -> str:
        return self.content.decode('utf-8')

    @functools.cached_property
    def json(self):
        return _helpers.json_loads(self.text)


def _compute_sha256(data: bytes):
    return base64.b64encode(hashlib.sha256(data).digest()).decode('utf-8')


def _get_url_route(url: urllib.parse.ParseResult):
    if len(url.query) > 0:
        return f'{url.path}?{url.query}'
    return url.path


def _get_required_headers(request: Request) -> typing.Iterator[tuple[str, str]]:
    yield '(request-target)', f'{request.method.name.lower()} {_get_url_route(request.url)}'
    yield 'date', email.utils.formatdate(usegmt=True)
    yield 'host', request.url.netloc

    if request.method.has_body:
        match request.content_type:
            case ContentType.JSON:
                content_type = 'application/json'
            case ContentType.OCTET_STREAM:
                content_type = 'application/octet-stream'

        yield 'content-length', str(len(request.content))
        yield 'content-type', content_type
        yield 'x-content-sha256', _compute_sha256(request.content)


@dataclasses.dataclass
class Client:
    tenant_id: str
    user_id: str
    api_key_fingerprint: str
    api_key_private_rsa: rsa.RSAPrivateKey
    service_endpoints: dict[str, pydantic.HttpUrl]
    region: str
    http_client: aiohttp.ClientSession

    @classmethod
    @contextlib.asynccontextmanager
    async def from_config(cls, config: cfg.Config):
        api_private_key = serialization.load_pem_private_key(
            _helpers.get_bytes(config.api_key.pem_private_key, encoding='ascii'), None
        )
        assert isinstance(api_private_key, rsa.RSAPrivateKey)
        async with _helpers.make_http_client() as http_client:
            yield cls(
                tenant_id=config.tenant_id,
                user_id=config.user_id,
                api_key_fingerprint=config.api_key.fingerprint,
                api_key_private_rsa=api_private_key,
                region=config.region,
                service_endpoints=get_bundled_service_endpoints(config.region)
                | await try_get_hosted_service_endpoints(http_client, config.region),
                http_client=http_client,
            )

    @classmethod
    @contextlib.asynccontextmanager
    async def new(
        cls,
        region: str,
        tenant_id: str,
        user_id: str,
        api_key_fingerprint: str,
        api_key_pem_private_key: bytes,
    ):
        async with cls.from_config(
            cfg.Config(
                region=region,
                tenant_id=tenant_id,
                user_id=user_id,
                api_key=cfg.ApiKey(
                    fingerprint=api_key_fingerprint, pem_private_key=api_key_pem_private_key
                ),
            )
        ) as client:
            yield client

    def _get_signature(self, required_headers: dict[str, str]):
        return 'Signature ' + ','.join(
            f'{k}="{v}"'
            for (k, v) in {
                'algorithm': 'rsa-sha256',
                'version': 1,
                'headers': ' '.join(required_headers),
                'keyId': f'{self.tenant_id}/{self.user_id}/{self.api_key_fingerprint}',
                'signature': base64.b64encode(
                    self.api_key_private_rsa.sign(
                        '\n'.join(f'{k}: {v}' for (k, v) in required_headers.items()).encode(
                            'ascii'
                        ),
                        padding.PKCS1v15(),
                        SHA256(),
                    )
                ).decode('ascii'),
            }.items()
        )

    def _get_headers_to_add(self, request: Request):
        required_headers = dict(_get_required_headers(request))
        return {
            'authorization': self._get_signature(required_headers),
            **{k: v for k, v in required_headers.items() if not k.startswith('(')},
        }

    async def request(
        self,
        *,
        service: str,
        method: HttpMethod,
        route: str,
        body: _helpers.JsonValue | bytes,
        output_file: typing.BinaryIO | None,
    ):
        if isinstance(body, bytes):
            content = body
            content_type = ContentType.OCTET_STREAM
        else:
            content = _helpers.json_dumps(body).encode('utf-8')
            content_type = ContentType.JSON

        endpoint = self.service_endpoints.get(service.lower())
        if endpoint is None:
            raise RuntimeError(f'Service {service} is not available in region {self.region}')

        url = f"{endpoint}{route.removeprefix('/')}"

        request = Request(
            method=method,
            url=urllib.parse.urlparse(url),
            content=content,
            content_type=content_type,
        )
        headers = self._get_headers_to_add(request)

        async with self.http_client.request(
            method=method.name, url=url, data=request.content, headers=headers
        ) as response:
            if response.status == 200 and output_file is not None:
                async for chunk in response.content.iter_chunked(1 << 20):
                    output_file.write(chunk)
                content = b''
            else:
                content = await response.content.read()
            return Response(
                status_code=response.status, headers=dict(response.headers), content=content
            )


def extract_service_endpoint_map(
    service_region_endpoint_map: _services.ServiceRegionEndpointMap, region: str
):
    return {
        service: endpoint
        for service, region_endpoint_map in service_region_endpoint_map.values.items()
        if (endpoint := region_endpoint_map.get(region.lower())) is not None
    }


def get_bundled_service_endpoints(region: str):
    return extract_service_endpoint_map(_services.get_bundled_service_region_endpoint_map(), region)


async def try_get_hosted_service_endpoints(
    http_client: aiohttp.ClientSession, region: str
) -> dict[str, pydantic.HttpUrl]:
    with contextlib.suppress(aiohttp.ClientError, pydantic.ValidationError):
        return extract_service_endpoint_map(
            await _services.get_service_region_endpoint_map(http_client), region
        )
    return {}
