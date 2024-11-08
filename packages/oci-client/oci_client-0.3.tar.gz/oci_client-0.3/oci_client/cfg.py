import json
import pathlib
import tomllib

import pydantic

from oci_client import _helpers


class ApiKey(pydantic.BaseModel):
    fingerprint: str
    pem_private_key: bytes


class Config(pydantic.BaseModel):
    region: str
    tenant_id: str
    user_id: str
    api_key: ApiKey

    @staticmethod
    def from_toml(path_or_file: pathlib.Path | _helpers.SupportsRead[bytes]):
        if isinstance(path_or_file, pathlib.Path):
            with path_or_file.open(mode='rb') as f:
                return _config_from_toml(f)
        else:
            return _config_from_toml(path_or_file)

    @staticmethod
    def from_json(path_or_file: pathlib.Path | _helpers.SupportsRead[str | bytes]):
        if isinstance(path_or_file, pathlib.Path):
            with path_or_file.open(mode='r') as f:
                return _config_from_json(f)
        else:
            return _config_from_json(path_or_file)


def _config_from_toml(file: _helpers.SupportsRead[bytes]):
    return Config(**tomllib.load(file))


def _config_from_json(file: _helpers.SupportsRead[str | bytes]):
    return Config(**json.load(file))
