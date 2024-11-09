import os
import json
from typing import Union

Json = Union[None, bool, int, float, str, list, dict]


def read_text_file(file_path: str, encoding: str = "utf-8") -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    file = open(file_path, "rt", encoding=encoding)
    content = file.read()
    file.close()
    return content


def read_text_file_or_none(file_path: str, encoding: str = "utf-8") -> str | None:
    if not os.path.exists(file_path):
        return None
    file = open(file_path, "rt", encoding=encoding)
    content = file.read()
    file.close()
    return content


def read_text_file_or_default(file_path: str, default: str = "", encoding: str = "utf-8") -> str:
    if not os.path.exists(file_path):
        return default
    file = open(file_path, "rt", encoding=encoding)
    content = file.read()
    file.close()
    return content


def write_text_file(file_path: str, content: str, encoding: str = "utf-8") -> None:
    file = open(file_path, "wt", encoding=encoding)
    file.write(content)
    file.close()


def read_json_file(file_path: str, encoding: str = "utf-8") -> Json:
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    file = open(file_path, "rt", encoding=encoding)
    content = json.load(file)
    file.close()
    return content


def read_json_file_or_none(file_path: str, encoding: str = "utf-8") -> Json | None:
    if not os.path.exists(file_path):
        return None
    file = open(file_path, "rt", encoding=encoding)
    content = json.load(file)
    file.close()
    return content


def read_json_file_or_default(file_path: str, default: Json = None, encoding: str = "utf-8") -> Json:
    if not os.path.exists(file_path):
        return default
    file = open(file_path, "rt", encoding=encoding)
    content = json.load(file)
    file.close()
    return content


def write_json_file(file_path: str, content: Json, indent: int = 4, ensure_ascii: bool = False, encoding: str = "utf-8") -> None:
    file = open(file_path, "wt", encoding=encoding)
    json.dump(content, file, indent=indent, ensure_ascii=ensure_ascii)
    file.close()
