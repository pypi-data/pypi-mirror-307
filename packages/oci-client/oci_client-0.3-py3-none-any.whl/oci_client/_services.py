import contextlib
import itertools
import json
import pathlib

import aiohttp
import pydantic


def camel_to_snake(s: str):
    return s[0].lower() + ''.join(
        ('_' if c1.islower() and c2.isupper() else '') + c2.lower()
        for c1, c2 in itertools.pairwise(s)
    ).lstrip('_')


def normalise_service_name(s: str):
    return '_'.join(
        camel_to_snake(part) for part in ''.join(c if c.isalnum() else ' ' for c in s).split()
    )


def get_endpoint_parts(endpoint: str):
    return endpoint.split('://')[-1].split('.')


class ServiceIndex(pydantic.BaseModel):
    endpoints: list[str]
    specs: list[str]

    def get_regions_endpoint_map(self) -> dict[str, pydantic.HttpUrl]:
        regions_endpoint_map: dict[str, pydantic.HttpUrl] = {}
        for endpoint in self.endpoints:
            region = next(
                (p for p in reversed(get_endpoint_parts(str(endpoint))) if p.count('-') == 2), None
            )
            if region is None:
                continue
            with contextlib.suppress(pydantic.ValidationError):
                regions_endpoint_map[region] = pydantic.HttpUrl(endpoint)

        return regions_endpoint_map


class ServicesIndex(pydantic.BaseModel):
    services: dict[str, ServiceIndex]


async def get_services(http_client: aiohttp.ClientSession):
    service_list_url = 'https://docs.oracle.com/en-us/iaas/api/specs/index.json'

    async with http_client.get(url=service_list_url) as response:
        text = (await response.content.read()).decode(encoding='utf-8')

        if response.status != 200:
            raise RuntimeError(f'{service_list_url} responsed {response.status} {text}')
        return ServicesIndex(services=json.loads(text))


class ServiceRegionEndpointMap(pydantic.BaseModel):
    values: dict[str, dict[str, pydantic.HttpUrl]]


async def get_service_region_endpoint_map(http_client: aiohttp.ClientSession):
    services = await get_services(http_client)
    return ServiceRegionEndpointMap(
        values={
            normalise_service_name(k): service.get_regions_endpoint_map()
            for k, service in services.services.items()
        }
    )


BUNDLED_SERVICE_REGION_ENDPOINT_MAP_PATH = (
    pathlib.Path(__file__).parent / 'bundled' / 'endpoints.json'
)


def get_bundled_service_region_endpoint_map():
    return ServiceRegionEndpointMap(
        **json.loads(BUNDLED_SERVICE_REGION_ENDPOINT_MAP_PATH.read_text(encoding='utf-8'))
    )


def set_bundled_service_region_endpoint_map(service_region_endpoint_map: ServiceRegionEndpointMap):
    return BUNDLED_SERVICE_REGION_ENDPOINT_MAP_PATH.write_text(
        service_region_endpoint_map.model_dump_json(indent=4), encoding='utf-8'
    )
