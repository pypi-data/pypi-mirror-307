from enum import Enum
from typing import Union


class Environment(Enum):
    Development = "development"
    Production = "production"


def get_environment(env_input: Union[str, Environment]) -> Environment:
    if isinstance(env_input, Environment):
        return env_input
    try:
        return Environment(env_input.lower())
    except ValueError:
        raise ValueError(f"Invalid environment: {env_input}")
