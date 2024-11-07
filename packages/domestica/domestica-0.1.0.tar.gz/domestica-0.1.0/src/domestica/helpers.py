import json
import re
from pathlib import Path
from typing import Any


def read_json(path: str) -> dict[str, Any]:
    """
    Reads a JSON file and returns a dictionary.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict[str, Any]: The dictionary containing the JSON data.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(data: Any, path: str) -> None:
    """
    Writes a dictionary to a JSON file.

    Args:
        data (dict[str, Any]): The dictionary to be written to the JSON file.
        path (str): The path to the JSON file.
    """

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def clean_string(text: str) -> str:
    """
    Cleans the input string by removing special characters and
    leading/trailing white spaces.

    Args:
        text (str): The input string to be cleaned.

    Returns:
        str: The cleaned string, with special characters removed and
        leading/trailing spaces stripped.
    """
    pattern = r"[ºª]|[^\w\s]"
    return re.sub(pattern, "", text).strip()
