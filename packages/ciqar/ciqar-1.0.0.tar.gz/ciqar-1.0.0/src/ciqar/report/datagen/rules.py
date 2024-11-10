"""
Definition of the generator classes for creating the "by rule" view data.
"""

from __future__ import annotations

from copy import copy
from typing_extensions import override

from ciqar.input import Violation
from ciqar.report.datagen import FileRenderInformation, RenderInformationGeneratorConfig
from ciqar.report.datagen._base import FileListRenderInfoGenerator, RuleRenderInfoGenerator
from ciqar.templates.api import RuleListRow


class RuleListRenderInfoGenerator(RuleRenderInfoGenerator):
    """
    Generator that produces render information for the list of all linter rules.
    There is only one rule list, so this iterator stops after one iteration.
    """

    def __init__(
        self,
        generator_config: RenderInformationGeneratorConfig,
    ):
        super().__init__(generator_config=generator_config)
        self.__violations_by_rules = self._get_violations_by_rules()
        self.__iteration_done = False

    @override
    def __next__(self) -> FileRenderInformation:
        # This iterator instance returns exactly one item
        if self.__iteration_done:
            raise StopIteration()
        self.__iteration_done = True

        report_file = copy(self._report_file_prototype)
        report_file.path_to_report_root = ""
        report_file.rule_list_data = self.__create_rule_list_data(self.__violations_by_rules)
        absolute_output_filepath = self._report_base_path.joinpath(
            self._get_output_file_name(self._input_template_name)
        )
        return FileRenderInformation(
            input_template_name=self._input_template_name,
            output_file_path=absolute_output_filepath,
            template_data=report_file,
        )

    def __create_rule_list_data(
        self, violations_by_rules: dict[str, list[Violation]]
    ) -> list[RuleListRow]:
        rule_list_data = []
        for rule_name, violation_list in violations_by_rules.items():
            violation_count = len(violation_list)
            example_violation_message = violation_list[0].message_text if violation_list else ""
            rule_list_data.append(
                RuleListRow(
                    rule_name=rule_name,
                    violation_count=violation_count,
                    example_message=example_violation_message,
                )
            )
        return rule_list_data


class RuleDetailsRenderInfoGenerator(FileListRenderInfoGenerator, RuleRenderInfoGenerator):
    """
    Generator that produces render information for rule details pages.
    These pages contain a list of all files that caused a violation of their respective rules.
    Each iteration returns data for one rule page.
    """

    def __init__(self, generator_config: RenderInformationGeneratorConfig):
        super().__init__(generator_config=generator_config)
        self.__source_file_list = list(self._source_files)
        self.__violations_by_rules = self._get_violations_by_rules()
        self.__rule_iter = iter(self.__violations_by_rules.items())

    @override
    def __next__(self) -> FileRenderInformation:
        rule_name, violation_list = next(self.__rule_iter)
        report_file = copy(self._report_file_prototype)
        report_file.path_to_report_root = "../"
        report_file.context_name = rule_name
        affected_source_files = [v.filename for v in violation_list]
        report_file.file_list_data = self._create_source_file_list_data(
            [sf for sf in self.__source_file_list if sf.absolute_path in affected_source_files],
            violation_list,
        )
        absolute_output_filepath = self._report_base_path.joinpath(
            "rules", "{}{}".format(rule_name, self._get_output_file_suffix())
        )
        return FileRenderInformation(
            input_template_name=self._input_template_name,
            output_file_path=absolute_output_filepath,
            template_data=report_file,
        )
