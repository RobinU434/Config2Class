from dataclasses import dataclass

from config2class.api.base import StructuredConfig


@dataclass
class _Credentials(StructuredConfig):
    username: str
    password: str


@dataclass
class _Database(StructuredConfig):
    host: str
    port: int
    credentials: _Credentials

    def __post_init__(self):
        self.credentials = _Credentials(**self.credentials)  # pylint: disable=E1134


@dataclass
class _Caching(StructuredConfig):
    enabled: bool
    cache_size: int


@dataclass
class _Features(StructuredConfig):
    authentication: bool
    caching: _Caching

    def __post_init__(self):
        self.caching = _Caching(**self.caching)  # pylint: disable=E1134


@dataclass
class App_config(StructuredConfig):
    name: str
    version: str
    database: _Database
    features: _Features

    def __post_init__(self):
        self.database = _Database(**self.database)  # pylint: disable=E1134
        self.features = _Features(**self.features)  # pylint: disable=E1134
