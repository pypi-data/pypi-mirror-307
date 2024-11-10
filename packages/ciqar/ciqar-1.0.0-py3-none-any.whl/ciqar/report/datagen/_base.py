"""
Contains base classes for render data generator implementations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Sequence

from ciqar.input import SourceFile, Violation
from ciqar.report.datagen import FileRenderInformation, RenderInformationGeneratorConfig
from ciqar.templates.api import FileListRow


class RenderInformationGenerator(Iterator[FileRenderInformation]):
    """
    Base class of all render data generators.

    A "render data generator" is an iterator producing instances of FileRenderInformation from
    the given configuration. Each concrete implementation represents a certain view (or "page")
    of the report and produces the data needed to render report files from a specific template.
    Each iteration produces the data for a single report file.

    This base class does not enhance the Iterator interface but provides some common properties
    and methods for all generator implementations.
    """

    def __init__(self, generator_config: RenderInformationGeneratorConfig):
        super().__init__()
        self._report_base_path = generator_config.report_base_path
        self._source_files = generator_config.source_files
        self._violations = generator_config.violations
        self._report_file_prototype = generator_config.report_file_prototype
        self._input_template_name = generator_config.input_template_name
        self._global_messages = generator_config.global_messages
        self._analyzer_name = generator_config.analyzer_name

    def _get_relative_url_to_report_root(self, absolute_output_filepath: Path) -> str:
        """
        Returns the relative path from this report's output file to the report root.
        Derived classes may provide this path to the template which may need it for generating
        links to other report files.

        :return: Plain, relative URL path from the current output file to the report root
                 (e.g. "../../").
        """
        relative_filepath = absolute_output_filepath.relative_to(self._report_base_path)
        path_to_report_root = "../" * len(relative_filepath.parent.parts)
        return path_to_report_root

    def _create_corresponding_report_output_file_path(
        self, project_relative_file_path: Path
    ) -> Path:
        """
        Return the relative report file name that corresponds to the given (project relative)
        source file path.
        The original source tree is duplicated in the report (starting with the project base
        dir), just replacing the file suffix with the destination's one (e.g. ".html").

        :param project_relative_file_path: Original file path, relative to the project root.
        :return: Corresponding destination file path in the report output (relative to the
                 report root).
        """
        return project_relative_file_path.with_suffix(self._get_output_file_suffix())

    def _get_output_file_suffix(self) -> str:
        """
        Returns the file name suffix that shall be used for destination report files.
        This information is taken from the template file name. The provided suffix includes a
        leading dot.

        :return: File name suffix to use for generated report files.
        """
        return Path(Path(self._input_template_name).stem).suffix

    def _get_output_file_name(self, template_file_name: str) -> str:
        """
        Returns the default output file name for the requested template name, for cases when
        there is only one output file to generate for this template.

        :return: Outpout file name to use for the file generated from the given template.
        """
        # Simply strip the ".in" file name suffix
        return (
            template_file_name[:-3]
            if template_file_name.endswith(".in")
            else template_file_name
        )


class FileListRenderInfoGenerator(RenderInformationGenerator):
    """
    Base class for render data generators that create a list of source files.
    """

    def _create_source_file_list_data(
        self, source_files: Sequence[SourceFile], violations: Sequence[Violation]
    ) -> list[FileListRow]:
        """
        Generates file list data for the provided source files and violations. The returned list
        can be used for the `ReportFile.file_list_data` property.
        """

        violations_by_files: dict[Path, list[Violation]] = {}
        for violation in violations:
            violations_by_files.setdefault(violation.filename, []).append(violation)

        file_list_data = []
        for source_file in source_files:
            this_file_violations = violations_by_files.get(source_file.absolute_path, [])
            violation_count = len(this_file_violations)
            line_count = len({v.linenumber for v in this_file_violations})
            rating = 2
            if violation_count == 0:
                rating = 0
            elif violation_count < 10:
                rating = 1

            file_list_data.append(
                FileListRow(
                    display_filename=str(source_file.project_relative_path),
                    report_filename=str(
                        Path("sources").joinpath(
                            self._create_corresponding_report_output_file_path(
                                source_file.project_relative_path
                            )
                        )
                    ),
                    line_count=source_file.line_count,
                    bad_line_count=line_count,
                    violation_count=violation_count,
                    rating=rating,
                )
            )
        return file_list_data


class RuleRenderInfoGenerator(RenderInformationGenerator):
    """
    Base class for render data generators that work on rules.
    """

    def _get_violations_by_rules(self) -> dict[str, list[Violation]]:
        """
        Groups all violations of this generator by their rules.

        :return: Violations mapped to their rule names.
        """

        violations_by_rules: dict[str, list[Violation]] = {}
        for violation in self._violations:
            violations_by_rules.setdefault(violation.rule_id, []).append(violation)
        return violations_by_rules
