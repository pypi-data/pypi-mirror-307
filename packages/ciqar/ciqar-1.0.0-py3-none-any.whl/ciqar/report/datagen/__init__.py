"""
Input and output types of the template data generators.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence

from ciqar.input import SourceFile, Violation
from ciqar.templates.api import ReportFile


@dataclass
class RenderInformationGeneratorConfig:
    """
    Represents the generic/common configuration of all file render data generators.
    This is the common input type of all generators, but some may need additional data.
    """

    report_base_path: Path
    report_file_prototype: ReportFile
    input_template_name: str
    source_files: Sequence[SourceFile]
    analyzer_name: str
    violations: Sequence[Violation]
    global_messages: list[str]


@dataclass
class FileRenderInformation:
    """
    Represents a single report file that needs to be rendered from a (Jinja2) template.
    This it the output type of all template data generators, each iteration of a data generator
    produces one instance of this type.
    """

    input_template_name: str
    """ Name of the (Jinija) template file to render. """

    output_file_path: Path
    """ (Absolute) destination path of the generated file. """

    template_data: ReportFile
    """ Data to be provided to the Jinja2 template for rendering """
