import json
import os

__all__ = ["jread", "jwrite", "jupdate", "jappend", "jtouch"]


def jread(file_path: str, utf8: bool = False) -> dict:
    """
    Read a JSON file and return its contents as a dictionary.
    """
    args = {"encoding": "utf-8"} if utf8 else {}

    with open(file_path, "r", **args) as f:
        return json.load(f)


def jwrite(file_path: str, data: dict | list, utf8: bool = False) -> None:
    """
    Write a dictionary to a JSON file.
    """
    args = {"ensure_ascii": False} if utf8 else {}

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4, **args)


def jupdate(file_path: str, data: dict | list, utf8: bool = False) -> None:
    """
    Update a JSON file with new data.
    """
    args = {"encoding": "utf-8"} if utf8 else {}

    with open(file_path, "r", **args) as f:
        existing_data = json.load(f)

    assert isinstance(existing_data, dict), "Existing data must be a dictionary"
    existing_data.update(data)

    args = {"ensure_ascii": False} if utf8 else {}

    with open(file_path, "w") as f:
        json.dump(existing_data, f, indent=4, **args)


def jappend(file_path: str, data: dict | list, utf8: bool = False) -> None:
    """
    Append new data to a JSON file.
    """
    args = {"encoding": "utf-8"} if utf8 else {}

    with open(file_path, "r", **args) as f:
        existing_data = json.load(f)

    assert isinstance(existing_data, list), "Existing data must be a list"

    existing_data.append(data)

    args = {"ensure_ascii": False} if utf8 else {}

    with open(file_path, "w", **args) as f:
        json.dump(existing_data, f, indent=4, **args)


def jtouch(
    file_path: str, utf8: bool = False, defaultContent: dict | list = {}
) -> None:
    """
    Create a new JSON file with an empty dictionary.
    """
    if os.path.exists(file_path):
        return

    args = {"encoding": "utf-8"} if utf8 else {}
    with open(file_path, "w", **args) as f:
        json.dump(defaultContent, f, indent=4, **args)
