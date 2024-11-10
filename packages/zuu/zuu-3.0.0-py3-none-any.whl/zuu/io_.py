import os
import tomllib
import csv
from .json_ import jread, jwrite

__all__ = ["read", "write"]


def read(path: str):
    assert os.path.exists(path), "Path does not exist"
    match os.path.splitext(path)[1]:
        case ".toml":
            with open(path, "rb") as f:
                return tomllib.load(f)
        case ".json":
            return jread(path, True)
        case ".yml" | ".yaml":
            return _read_yaml(path)
        case ".env":
            return _read_env(path)
        case ".csv":
            return _read_csv(path)
        case _:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()


def _read_yaml(path):
    import yaml

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _read_env(path):
    try:
        import pydotenv

        env = pydotenv.Environment(path)
        return dict(env)
    except ImportError:
        raw = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    raw[k] = v


def _read_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.reader(f))


def write(
    path: str,
    data: str | dict | list,
):
    assert os.path.exists(path), "Path does not exist"
    match os.path.splitext(path)[1]:
        case ".toml":
            return _write_toml(path, data)
        case ".json":
            return jwrite(path, data, utf8=True)
        case ".yml" | ".yaml":
            return _write_yaml(path, data)
        case ".env":
            return _write_env(path, data)
        case ".csv":
            return _write_csv(path, data)
        case _:
            with open(path, "w", encoding="utf-8") as f:
                return f.write(data)


def _write_toml(path, data):
    try:
        import toml

        with open(path, "w", encoding="utf-8") as f:
            return toml.dump(data, f)
    except ImportError:
        raise ImportError("toml is not installed")


def _write_yaml(path, data):
    try:
        import yaml

        with open(path, "w", encoding="utf-8") as f:
            return yaml.dump(data, f)
    except ImportError:
        raise ImportError("yaml is not installed")


def _write_env(path, data):
    assert isinstance(data, dict), "data must be a dictionary"

    with open(path, "w", encoding="utf-8") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")


def _write_csv(path, data):
    assert isinstance(data, list), "data must be a list"
    with open(path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        return writer.writerows(data)
