"""
Definition of the SummaryRenderInfoGenerator class.
"""

from __future__ import annotations

from copy import copy
from datetime import datetime
import time
from typing_extensions import override

from ciqar.report.datagen import FileRenderInformation, RenderInformationGeneratorConfig
from ciqar.report.datagen._base import RenderInformationGenerator
from ciqar.templates.api import SummaryData


class SummaryRenderInfoGenerator(RenderInformationGenerator):
    """
    Generator that produces render information for a check summary page.
    There is only one summary, so this iterator stops after one iteration.
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
        report_file.summary_data = self.__create_summary_data()
        absolute_output_filepath = self._report_base_path.joinpath(
            self._get_output_file_name(self._input_template_name)
        )

        return FileRenderInformation(
            input_template_name=self._input_template_name,
            output_file_path=absolute_output_filepath,
            template_data=report_file,
        )

    def __create_summary_data(self) -> SummaryData:
        timestring = "{0} ({1})".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), time.tzname[time.daylight]
        )
        source_file_list = list(self._source_files)
        violation_list = list(self._violations)
        bad_line_count = len({hash((v.filename, v.linenumber)) for v in violation_list})

        summary_data = SummaryData(
            source_file_count=len(source_file_list),
            violation_count=len(violation_list),
            line_count=sum(sf.line_count for sf in source_file_list),
            bad_line_count=bad_line_count,
            generation_time=timestring,
            analyzer_tag=self._analyzer_name,
            global_linter_messages=self._global_messages,
        )
        return summary_data
