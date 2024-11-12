import os
try:
    import tomllib as toml
except ImportError:
    import tomli as toml


class TomlEnvError(Exception):
    pass


class EnvObject(object):
    true_values = ["True", "true", 1, "1"]
    false_values = ["False", "false", 0, "0"]
    bool_values = true_values + false_values

    def __init__(self, data: dict, override: bool=False):
        self.data = data
        self.override = override

    def get(self, key, default=None, nullable=False):
        result = os.environ.get(key)
        if result is not None and not self.override:
            return result
        if key not in self.data:
            if default is not None:
                result = default
            elif nullable:
                result = None
            elif result is None:
                raise TomlEnvError(f"'{key}' not found in environment")
        else:
            result = self.data[key]
        return result

    def get_str(self, key, default=None, nullable=False):
        r = self.get(key, default=default, nullable=nullable)
        if r is None:
            return None
        return str(r)


    def get_int(self, key, default=None, nullable=False):
        r = self.get(key, default=default, nullable=nullable)
        if r is None:
            return None
        return int(r)

    def get_float(self, key, default=None, nullable=False):
        r = self.get(key, default=default, nullable=nullable)
        if r is None:
            return None
        return float(r)

    def get_bool(self, key, default=False, nullable=False):
        value = self.get(key, default=default, nullable=nullable)
        if value not in self.bool_values:
            raise TomlEnvError(f"'{key}={value}' is not a boolean value")
        return value in self.true_values


def load_env(path: str = ".env.toml", override: bool = False) -> EnvObject:
    with open(path, "rb") as f:
        data = toml.load(f)
    if "ENV" not in os.environ:
        raise TomlEnvError("The environment variable 'ENV' is not set")
    env_name = os.environ["ENV"]
    if env_name not in data:
        raise TomlEnvError(f"ENV '{env_name}' not found in {path}")
    return EnvObject(data[env_name], override=override)
