from .json_schema_template import JsonSchemaOptions as schema
from .json_template import JsonOptions as json
from .mpck_template import MpckOptions as mpck
from .toml_template import TomlOptions as toml
from .yaml_template import YamlOptions as yaml


__version__ = 'v1.0.0'


__all__ = [
    "schema",
    "json",
    "mpck",
    "toml",
    "yaml",
    "__version__"]
