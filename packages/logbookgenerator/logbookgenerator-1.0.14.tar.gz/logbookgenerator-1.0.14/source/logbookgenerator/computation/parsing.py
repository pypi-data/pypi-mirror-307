"""parsing.py: Contains the functions for parsing the input directory."""

import os
import re
from pathlib import Path

from ..config.constants import Constants
from ..utilities.file_handling import load_yaml
from . import logger

logger = logger.getChild(__name__)


def parse_weekly_directories(
    input_directory: Path,
) -> tuple[list[dict[str, dict[str, str] | str]], dict[str, str]]:
    """
    Parse the weeks directory.

    Parameters
    ----------
    input_directory : Path
        Path to the input directory.

    Returns
    -------
    tuple[list[dict[str, dict[str, str] | str]], dict[str, str]]
        The CPP files and reflections for each week, given as a list of weeks,
        where each week has keys "cpp" and "reflection", each containing a
        dictionary of files or a string respectively.
        Also returns the coursework files.
    """
    weeks_files: list[dict[str, dict[str, str] | str]] = []
    coursework_files: dict[str, str] = {}

    # Get the weeks, organised chronologically so that the dictionary is ordered
    weeks = sorted(
        [
            directory
            for directory in os.listdir(input_directory)
            if directory.startswith("week") and (input_directory / directory).is_dir()
        ]
    )
    logger.debug(f"Weeks found: {weeks}")

    for week in weeks:
        week_files: dict[str, dict[str, str] | str] = {
            "cpp": {},
            "reflection": "",
        }
        week_path = input_directory / week
        logger.debug(f"Reading week from {week_path}")

        # Parse CPP files
        for file_path in week_path.glob("*.cpp"):
            with open(file_path) as file:
                file_contents = file.read()
                logger.debug(f"Read file {file_path}")

                # Add the file to the week
                week_files["cpp"][file_path.stem] = file_contents  # type: ignore
                logger.debug(f"Added file {file_path} to week")

                # Check if the file is coursework
                if match := re.match(Constants.COURSEWORK_REGEX, file_path.stem):
                    # Add the coursework file to the list
                    coursework_files[match.group(1)] = file_contents
                    logger.debug(f"Added file {file_path} to coursework")

        # Parse reflection
        reflection_path = week_path / "reflection.md"
        with open(reflection_path) as file:
            week_files["reflection"] = file.read()
            logger.debug(f"Read reflection {reflection_path}")

        # Add the week to the list
        weeks_files.append(week_files)

    return weeks_files, coursework_files


def parse_input_directory(
    input_directory: Path,
) -> tuple[list[dict[str, dict[str, str] | str]], dict[str, str], list[dict[str, str]]]:
    """
    Parse the input directory.

    Parameters
    ----------
    input_directory : Path
        Path to the input directory.

    Returns
    -------
    tuple[list[dict[str, dict[str, str] | str]], dict[str, str], list[dict[str, str]]]
        The weekly files (code and reflections), coursework files, and references.
    """
    logger.debug(f"Reading weeks from {input_directory}")
    weeks, coursework = parse_weekly_directories(input_directory)
    logger.debug(f"Read weeks: {weeks}")
    logger.debug(f"Read coursework: {coursework}")

    references_path = input_directory / "references.yaml"
    logger.debug(f"Reading references from {references_path}")
    references_dictionary = load_yaml(references_path)
    references = references_dictionary["references"]
    logger.debug(f"Read references: {references}")

    return weeks, coursework, references
