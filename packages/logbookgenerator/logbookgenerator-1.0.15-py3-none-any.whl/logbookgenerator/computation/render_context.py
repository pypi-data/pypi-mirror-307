"""render_context.py: Contains the logic for rendering the context into a logbook."""

from pathlib import Path
from typing import Any

import jinja2

from ..config.paths import Paths
from . import logger

logger = logger.getChild(__name__)


def render_template(template_path: Path, context: dict[str, Any]) -> str:
    """
    Render the template with the context.

    Parameters
    ----------
    template_path : Path
        Path to the template.
    context : dict[str, Any]
        Context to render the template.

    Returns
    -------
    str
        Rendered template.

    Raises
    ------
    FileNotFoundError
        If the template does not exist.
    jinja2.exceptions.TemplateSyntaxError
        If there is a syntax error in the template.
    """
    if not template_path.exists():
        logger.error(f"Template at {template_path} does not exist.")
        raise FileNotFoundError(f"Template at {template_path} does not exist.")

    try:
        logger.debug(f"Rendering the template at {template_path}.")
        with open(template_path) as file:
            template = jinja2.Template(file.read())

        rendered_template = template.render(context)
    except jinja2.exceptions.TemplateSyntaxError as e:
        logger.error(f"Error in the template at {template_path}: {e}")
        raise e
    except ValueError as e:
        logger.error(f"Error in the context for the template at {template_path}: {e}")
        logger.error(f"Context: {context}")
        raise e

    logger.debug(f"Rendered the template at {template_path}.")
    return rendered_template


def create_logbook(logbook_contexts: dict[str, Any]) -> str:
    """
    Create the logbook from the contexts.

    Parameters
    ----------
    logbook_contexts : dict
        The contexts to render into the logbook.

    Notes
    -----
    This function renders each part of the logbook and then combines them into
    the final markdown logbook.
    """
    logger.debug("Rendering the logbook.")
    logbook_markdown = ""

    logger.debug("Rendering the logbook cover.")
    logbook_markdown += (
        render_template(
            Paths.TEMPLATES_PATH / "cover.md.j2",
            logbook_contexts["cover"],
        )
        + "\n\n"
    )

    logger.debug("Rendering the logbook table of contents.")
    logbook_markdown += (
        render_template(
            Paths.TEMPLATES_PATH / "contents.md.j2",
            {"weeks": logbook_contexts["weeks"]},
        )
        + "\n\\newpage\n"
    )

    logger.debug("Rendering the logbook weekly entries.")
    for week in logbook_contexts["weeks"].values():
        logger.debug(f"Rendering week {week['number']} with context {week}.")
        logbook_markdown += (
            render_template(
                Paths.TEMPLATES_PATH / "week.md.j2",
                week,
            )
            + "\n\\newpage\n"
        )
        logger.debug(f"Rendered week {week['number']}.")

    logger.debug("Rendering the logbook references.")
    logbook_markdown += render_template(
        Paths.TEMPLATES_PATH / "references.md.j2",
        {"references": logbook_contexts["references"]},
    )

    return logbook_markdown


def create_coursework(coursework_context: dict[str, Any]) -> str:
    """
    Create the coursework from the context.

    Parameters
    ----------
    coursework_context : dict
        The contexts to render into the coursework.

    Notes
    -----
    This function renders each part of the coursework and then combines them into
    the final markdown coursework.
    """
    logger.debug("Rendering the coursework.")
    coursework_markdown = ""

    for file_name, file_context in coursework_context.items():
        logger.debug(f"Rendering coursework for {file_name}.")
        coursework_markdown += (
            render_template(
                Paths.TEMPLATES_PATH / "coursework.md.j2",
                {
                    "file_name": file_name,
                    "tasks": file_context,
                },
            )
            + "\n\n"
        )
        logger.debug(f"Rendered coursework for {file_name}.")

    return coursework_markdown
