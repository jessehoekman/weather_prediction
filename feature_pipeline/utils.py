import json
import logging
from pathlib import Path
from typing import Any, Union

from feature_pipeline import settings


def get_logger(name: str) -> logging.Logger:
    """Template for getting a logger.

    Args:
    ----
        name: Name of the logger.

    Returns: Logger.

    """
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)


def save_json(
    data: dict,
    file_name: str,
    save_dir: Union[Path, str] = settings.OUTPUT_DIR,
) -> None:
    """Save a dictionary as a JSON file.

    Args:
    ----
        data: data to save.
        file_name: Name of the JSON file.
        save_dir: Directory to save the JSON file.

    Returns: None

    """
    data_path = Path(save_dir) / file_name
    with Path.open(data_path, "w") as f:
        json.dump(data, f)


def load_json(file_name: str, save_dir: Union[Path, str] = settings.OUTPUT_DIR) -> Any:
    """Load a JSON file.

    Args:
    ----
        file_name: Name of the JSON file.
        save_dir: Directory of the JSON file.

    Returns: Dictionary with the data.

    """
    data_path = Path(save_dir) / file_name
    if not data_path.exists():
        msg = f"Cached JSON from {data_path} does not exist."
        raise FileNotFoundError(msg)

    with Path.open(data_path) as f:
        return json.load(f)  # type: ignore[attr-defined]
