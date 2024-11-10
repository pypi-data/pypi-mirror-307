"""
Definition of the ListingsRenderInfoGenerator class.
"""

from __future__ import annotations

from copy import copy
from typing import Sequence
from typing_extensions import override

from ciqar.input import SourceFile, Violation
from ciqar.report.datagen import FileRenderInformation, RenderInformationGeneratorConfig
from ciqar.report.datagen._base import RenderInformationGenerator
from ciqar.templates.api import SourceLine


class ListingsRenderInfoGenerator(RenderInformationGenerator):
    """
    Generator that produces render information for source file listing pages.
    Each iteration returns data for one source file.
    """

    def __init__(self, generator_config: RenderInformationGeneratorConfig):
        super().__init__(generator_config=generator_config)
        self.__source_file_iter = iter(self._source_files)

    @override
    def __next__(self) -> FileRenderInformation:
        source_file = next(self.__source_file_iter)
        report_file = copy(self._report_file_prototype)
        absolute_output_filepath = self._report_base_path.joinpath(
            "sources",
            self._create_corresponding_report_output_file_path(
                source_file.project_relative_path
            ),
        )
        report_file.path_to_report_root = self._get_relative_url_to_report_root(
            absolute_output_filepath
        )
        report_file.context_name = str(source_file.project_relative_path)
        report_file.source_content_data = self.__create_source_content_data(
            source_file, self._violations
        )

        return FileRenderInformation(
            input_template_name=self._input_template_name,
            output_file_path=absolute_output_filepath,
            template_data=report_file,
        )

    def __create_source_content_data(
        self, source_file: SourceFile, violations: Sequence[Violation]
    ) -> list[SourceLine]:
        file_violations = [v for v in violations if v.filename == source_file.absolute_path]
        source_lines = []
        for idx, code in enumerate(source_file.content):
            lineno = idx + 1

            current_line_violations = [v for v in file_violations if v.linenumber == lineno]
            source_lines.append(
                SourceLine(
                    lineno=lineno,
                    content=code.rstrip("\n").rstrip("\r"),
                    rating="good" if not current_line_violations else "bad",
                    messages=[
                        "{}: {}".format(violation.severity, violation.message_text)
                        for violation in current_line_violations
                    ],
                )
            )
        return source_lines
