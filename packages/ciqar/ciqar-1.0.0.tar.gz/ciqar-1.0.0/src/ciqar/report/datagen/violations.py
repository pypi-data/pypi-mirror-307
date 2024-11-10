"""
Definition of the ViolationListRenderInfoGenerator class.
"""

from __future__ import annotations

from copy import copy
from typing import Sequence
from typing_extensions import override

from ciqar.input import SourceFile, Violation
from ciqar.report.datagen import FileRenderInformation, RenderInformationGeneratorConfig
from ciqar.report.datagen._base import RenderInformationGenerator
from ciqar.templates.api import ViolationListRow


class ViolationListRenderInfoGenerator(RenderInformationGenerator):
    """
    Generator that produces render information for a violations listing page.
    There is only one violations list, so this iterator stops after one iteration.
    """

    def __init__(self, generator_config: RenderInformationGeneratorConfig):
        super().__init__(generator_config=generator_config)
        self.__iteration_done = False

    @override
    def __next__(self) -> FileRenderInformation:
        if self.__iteration_done:
            raise StopIteration()

        self.__iteration_done = True
        report_file = copy(self._report_file_prototype)
        report_file.path_to_report_root = ""
        report_file.violation_list_data = self.__create_violation_list_data(
            list(self._source_files), self._violations
        )
        absolute_output_filepath = self._report_base_path.joinpath(
            self._get_output_file_name(self._input_template_name)
        )

        return FileRenderInformation(
            input_template_name=self._input_template_name,
            output_file_path=absolute_output_filepath,
            template_data=report_file,
        )

    def __create_violation_list_data(
        self,
        source_files: list[SourceFile],
        violations: Sequence[Violation],
    ) -> list[ViolationListRow]:
        """
        Generates violation list data for the provided violations. The returned list can
        be used for the `ReportFile.violation_list_data` property.
        """

        violation_list_row_data = []
        for violation in violations:
            source_file = next(f for f in source_files if f.absolute_path == violation.filename)
            violation_list_row_data.append(
                ViolationListRow(
                    display_filename=str(source_file.project_relative_path),
                    lineno=violation.linenumber,
                    rule=violation.rule_id,
                    message_lines=violation.message_text.split("\n"),
                )
            )
        violation_list_row_data.sort(key=lambda v: (v.display_filename, v.lineno))
        return violation_list_row_data
