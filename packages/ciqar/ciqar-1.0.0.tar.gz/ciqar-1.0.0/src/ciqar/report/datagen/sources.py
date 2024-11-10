"""
Definition of the SourceListRenderInfoGenerator class.
"""

from __future__ import annotations

from copy import copy
from typing_extensions import override

from ciqar.report.datagen import FileRenderInformation, RenderInformationGeneratorConfig
from ciqar.report.datagen._base import FileListRenderInfoGenerator


class SourceListRenderInfoGenerator(FileListRenderInfoGenerator):
    """
    Generator that produces render information for a source file listing page.
    There is only one source list, so this iterator stops after one iteration.
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
        report_file.file_list_data = self._create_source_file_list_data(
            self._source_files, self._violations
        )
        absolute_output_filepath = self._report_base_path.joinpath(
            self._get_output_file_name(self._input_template_name)
        )

        return FileRenderInformation(
            input_template_name=self._input_template_name,
            output_file_path=absolute_output_filepath,
            template_data=report_file,
        )
