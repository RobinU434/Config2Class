from dataclasses import dataclass
import config2class.utils.filesystem as fs_utils


from config2class.utils.replacement import replace_tokens


@dataclass
class _Credentials:
    username: str
    password: str

    @classmethod
    def from_file(cls, file: str) -> "_Credentials":
        ending = file.split('.')[-1]
        content = getattr(fs_utils, f'load_{ending}')(file)
        content = replace_tokens(content)
        first_key, first_value = content.popitem()
        if len(content) == 0 and isinstance(first_value, dict):
            return cls(**first_value)
        else:
            content[first_key] = first_value
        return cls(**content)


@dataclass
class _Database:
    host: str
    port: int
    credentials: _Credentials

    @classmethod
    def from_file(cls, file: str) -> "_Database":
        ending = file.split('.')[-1]
        content = getattr(fs_utils, f'load_{ending}')(file)
        content = replace_tokens(content)
        first_key, first_value = content.popitem()
        if len(content) == 0 and isinstance(first_value, dict):
            return cls(**first_value)
        else:
            content[first_key] = first_value
        return cls(**content)

    def __post_init__(self):
        self.credentials = _Credentials(**self.credentials)  #pylint: disable=E1134


@dataclass
class _Caching:
    enabled: bool
    cache_size: int

    @classmethod
    def from_file(cls, file: str) -> "_Caching":
        ending = file.split('.')[-1]
        content = getattr(fs_utils, f'load_{ending}')(file)
        content = replace_tokens(content)
        first_key, first_value = content.popitem()
        if len(content) == 0 and isinstance(first_value, dict):
            return cls(**first_value)
        else:
            content[first_key] = first_value
        return cls(**content)


@dataclass
class _Features:
    authentication: bool
    caching: _Caching

    @classmethod
    def from_file(cls, file: str) -> "_Features":
        ending = file.split('.')[-1]
        content = getattr(fs_utils, f'load_{ending}')(file)
        content = replace_tokens(content)
        first_key, first_value = content.popitem()
        if len(content) == 0 and isinstance(first_value, dict):
            return cls(**first_value)
        else:
            content[first_key] = first_value
        return cls(**content)

    def __post_init__(self):
        self.caching = _Caching(**self.caching)  #pylint: disable=E1134


@dataclass
class App_config:
    name: str
    version: str
    database: _Database
    features: _Features

    @classmethod
    def from_file(cls, file: str) -> "App_config":
        ending = file.split('.')[-1]
        content = getattr(fs_utils, f'load_{ending}')(file)
        content = replace_tokens(content)
        first_key, first_value = content.popitem()
        if len(content) == 0 and isinstance(first_value, dict):
            return cls(**first_value)
        else:
            content[first_key] = first_value
        return cls(**content)

    def __post_init__(self):
        self.database = _Database(**self.database)  #pylint: disable=E1134
        self.features = _Features(**self.features)  #pylint: disable=E1134
