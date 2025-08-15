import json
from pathlib import Path

def load_config_file(file_path: Path):
    """
    Loads a JSON configuration file from the specified path.

    Args:
        file_path (Path): The path to the JSON configuration file.

    Returns:
        dict: The contents of the configuration file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """

    with open(file_path, mode='r', encoding='utf-8') as f:
        config_file = json.load(f)

    return config_file
