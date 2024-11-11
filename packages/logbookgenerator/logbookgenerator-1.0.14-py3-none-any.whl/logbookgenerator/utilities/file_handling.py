"""file_handling.py: Contains functions for handling files."""

from pathlib import Path
from typing import Any

import yaml

from . import logger

logger = logger.getChild(__name__)


def load_yaml(yaml_path: Path) -> dict[str, Any]:
    """
    Load the YAML file.

    Parameters
    ----------
    yaml_path : Path
        Path to the YAML file.

    Returns
    -------
    dict[str, Any]
        The YAML file as a dictionary.
    """
    with open(yaml_path) as file:
        try:
            logger.debug(f"Loading YAML file: {yaml_path}")
            yaml_dictionary: dict[str, Any] = yaml.safe_load(file)
            return yaml_dictionary
        except yaml.YAMLError as error:
            logger.error(f"Error loading YAML file: {error}")
            raise error


def save_file(file_path: Path, file_content: str) -> None:
    """
    Save the file.

    Parameters
    ----------
    file_path : Path
        Path to the file.
    file_content : str
        Content to save in the file.
    """
    # Create the parent directories if they do not exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the file
    with open(file_path, "w") as file:
        logger.debug(f"Saving file: {file_path}")
        file.write(file_content)


def create_clean_code_files(coursework_path: Path, clean_code: dict[str, str]) -> None:
    """
    Create the clean code files.

    Parameters
    ----------
    coursework_path : Path
        Path to the coursework directory.
    clean_code : dict[str, str]
        The clean code files.
    """
    for file_name, file_content in clean_code.items():
        save_file(coursework_path / file_name, file_content)
        logger.info(f"Clean code file created: {file_name} in {coursework_path}.")
