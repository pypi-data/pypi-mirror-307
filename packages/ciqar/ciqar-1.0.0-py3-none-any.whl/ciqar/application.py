from __future__ import annotations

from argparse import ArgumentParser, ArgumentTypeError
from functools import partial
from importlib import import_module
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

from ciqar.input.linter.mypy_logfile import MypyLogfileParser
from ciqar.input.linter.pyright_json import PyrightJsonParser
from ciqar.input.linter.result_parser import LinterResultParser
from ciqar.input.linter.ruff_json import RuffJsonParser
from ciqar.input.sourcefiles import SourceFileCollector
from ciqar.report.generator import ReportGenerator, TemplateMetadata
from ciqar.templates.api import TemplateFilesDescription


class CiqarApplication:
    """
    Represents the application itself.
    Central entry point is the `run()` method.
    """

    def __init__(self) -> None:
        self.__search_paths: list[Path]
        self.__output_path: Path
        self.__template_name: str
        self.__template_files_spec: TemplateFilesDescription

        self.__process_commandline()

    @property
    def application_name(self) -> str:
        """Name of the application."""
        return "Ciqar"

    @property
    def application_version(self) -> str:
        """Application version to be displayed to the user."""
        import ciqar

        return ciqar.__version__

    def __process_commandline(self) -> None:
        """
        Processes the command line parameters and sets/initializes all internal members
        accordingly. Must be run exactly once during initialization. May exit() if there are
        any errors (e.g. missing arguments).
        """
        cmd_parser = self.__configure_cmdline_parser()
        args = cmd_parser.parse_args()

        # Store source and output paths as absolute Paths
        self.__search_paths = [p.resolve() for p in args.source_paths]
        self.__exclude_paths = (
            [p.resolve() for p in args.exclude_paths] if args.exclude_paths else []
        )
        self.__output_path = args.output_path.resolve()
        self.__result_parser_factory = args.result_parser_factory
        self.__template_name, self.__template_files_spec = args.template_metadata

    @staticmethod
    def _parse_analyzer_result_url(
        analyzer_result_url: str,
    ) -> Callable[[], LinterResultParser]:
        """
        Parses the provided analyzer result URL into a factory for creating the corresponding
        result parser.

        :param analyzer_result_url: Analyzer URL as provided on the command line.
        :raises: ArgumentTypeError if the URL is invalid.
        """
        url = urlparse(analyzer_result_url)
        if not url.path.strip():
            raise ArgumentTypeError(
                "Analyzer result URL does not contain a path to a result file of the chosen "
                "analyzer."
            )

        analyzer_result_path = Path(url.path).resolve()
        result_parser_class: type[LinterResultParser]
        if url.scheme == "mypy":
            result_parser_class = MypyLogfileParser
        elif url.scheme == "pyright":
            result_parser_class = PyrightJsonParser
        elif url.scheme == "ruff":
            result_parser_class = RuffJsonParser
        else:
            raise ArgumentTypeError(
                "Analyzer result URL contains an invalid analyzer: '{}'.\n\tPlease use a "
                "URL-like string of the format 'analyzer:path'.".format(analyzer_result_url)
            )

        return partial(result_parser_class, analyzer_result_path)

    @staticmethod
    def _load_template_files_specification(
        template_name: str,
    ) -> tuple[str, TemplateFilesDescription]:
        """
        Loads the template metadata by the requested name and extracts the template file
        specification.

        :param template_name: Name of the template to load, as provided on the command line.
        :raises: ArgumentTypeError if the requested template is not found or does not provide
                 valid metadata.
        """

        template_module_path = f"ciqar.templates.{template_name}"
        try:
            metadata_module = import_module(template_module_path)
        except Exception:
            # Template module not found (e.g. ModuleNotFoundError)
            raise ArgumentTypeError(
                f"The chosen template '{template_name}' does not exist, please check your spelling."
            )
        try:
            template_files_specification: TemplateFilesDescription = (
                metadata_module.template_files_specification
            )
        except Exception:
            # Metadata definition is missing in module (e.g. AttributeError)
            raise ArgumentTypeError(
                f"The chosen template '{template_name}' seems to be broken because it does not "
                f"provide template metadata. It cannot be used, please choose another one."
            )
        return template_name, template_files_specification

    def __configure_cmdline_parser(self) -> ArgumentParser:
        """
        Sets up the commandline argument parser (defining arguments, help messages etc).
        Must be run exactly once during initialization.
        """
        parser = ArgumentParser(
            description=(
                "Create a report from the output of a code quality analyzer tool (e.g. MyPy)."
            )
        )
        parser.add_argument(
            "--version",
            action="version",
            version=f"{self.application_name} {self.application_version}",
            help="Show version number and exit.",
        )
        parser.add_argument(
            "-r",
            "--analyzer-result",
            dest="result_parser_factory",
            required=True,
            type=self._parse_analyzer_result_url,
            help="Analyzer result URL to generate a report from.",
        )
        parser.add_argument(
            "-s",
            "--source-path",
            dest="source_paths",
            action="append",
            required=True,
            type=Path,
            help=(
                "Path to look for analyzed source file into. May be provided several times, "
                "but all search directories must have a common ancestor."
            ),
        )
        parser.add_argument(
            "-e",
            "--exclude",
            dest="exclude_paths",
            action="append",
            required=False,
            type=Path,
            help=(
                "Path of a single file or a directory within one of the source paths to be "
                "excluded from the search for source files. May be provided several times."
            ),
        )
        parser.add_argument(
            "-o",
            "--output",
            dest="output_path",
            required=True,
            type=Path,
            help="Directory to write the generated report into.",
        )
        parser.add_argument(
            "-t",
            "--template",
            dest="template_metadata",
            metavar="TEMPLATE_NAME",
            required=False,
            type=self._load_template_files_specification,
            default="html_detailed",
            help="Name of the report template to use. Defaults to '%(default)s'.",
        )
        return parser

    def run(self) -> None:
        template_metadata = TemplateMetadata(
            template_name=self.__template_name,
            render_metadata=self.__template_files_spec,
        )
        generator = ReportGenerator(
            source_collector=SourceFileCollector(self.__search_paths, self.__exclude_paths),
            violations_parser=self.__result_parser_factory(),
            template_metadata=template_metadata,
            output_path=self.__output_path,
            application_tag=f"{self.application_name} version {self.application_version}",
        )
        generator.generate_report()
