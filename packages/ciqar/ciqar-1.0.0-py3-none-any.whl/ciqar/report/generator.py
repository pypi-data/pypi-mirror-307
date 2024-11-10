from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
from typing_extensions import assert_never

from ciqar.input.linter.result_parser import LinterResultParser
from ciqar.input.sourcefiles import SourceFileCollector
from ciqar.input.violations import LinterResultCollector
from ciqar.report.datagen import FileRenderInformation, RenderInformationGeneratorConfig
from ciqar.report.datagen._base import RenderInformationGenerator
from ciqar.report.datagen.listings import ListingsRenderInfoGenerator
from ciqar.report.datagen.rules import (
    RuleDetailsRenderInfoGenerator,
    RuleListRenderInfoGenerator,
)
from ciqar.report.datagen.sources import SourceListRenderInfoGenerator
from ciqar.report.datagen.summary import SummaryRenderInfoGenerator
from ciqar.report.datagen.violations import ViolationListRenderInfoGenerator
from ciqar.report.jinja_wrapper import JinjaWrapper
from ciqar.templates.api import RenderDataType, ReportFile, TemplateFilesDescription


@dataclass
class TemplateMetadata:
    """
    Describes the template to be used for the report generation.
    """

    template_name: str
    """
    Name of the template (refers to a directory name within `ciqar.templates`).
    """

    render_metadata: TemplateFilesDescription
    """
    Describes which files of the template need to be processed and how.
    """


class ReportGenerator:
    """
    Generates the report from the provided source files and linter results.
    This is meant to be very generic, the concrete details of the report generation are defined
    by the selected template. The actual generation of the data needed for rendering each
    template file is delegated to specific "data generators" that are derived from
    `RenderInformationGenerator`. This class is responsible for the creation of the output files
    and directories, though.
    """

    def __init__(
        self,
        source_collector: SourceFileCollector,
        violations_parser: LinterResultParser,
        template_metadata: TemplateMetadata,
        output_path: Path,
        application_tag: str,
    ):
        self.__source_collector = source_collector
        self.__violation_collector = LinterResultCollector(
            violations_parser, source_collector.get_excluded_source_files()
        )
        self.__template_render_metadata = template_metadata.render_metadata
        self.__jinja_wrapper = JinjaWrapper(template_metadata.template_name)
        self.__output_path = output_path
        self.__report_name = "{} Code Quality Report".format(
            self.__violation_collector.get_analyzer_name()
        )
        self._application_tag = application_tag

    def generate_report(self) -> None:
        self.__prepare_output_dir()

        # 1. Create all report files
        report_file_prototype = self.__create_report_file_prototype()
        for input_file_name, render_data_type in self.__template_render_metadata[
            "render_files"
        ].items():
            GeneratorClass = self._get_generator_class(render_data_type)
            generator_config = RenderInformationGeneratorConfig(
                report_base_path=self.__output_path,
                report_file_prototype=report_file_prototype,
                input_template_name=input_file_name,
                analyzer_name=self.__violation_collector.get_analyzer_name(),
                source_files=self.__source_collector.get_all_source_files(),
                violations=self.__violation_collector.get_all_violations(),
                global_messages=self.__violation_collector.get_global_messages(),
            )

            render_data_generator = GeneratorClass(generator_config)
            for render_information in render_data_generator:
                self.__generate_template_file(render_information)

        # 2. Copy all static files into the output directory
        for static_file in self.__template_render_metadata["static_files"]:
            static_file_path = self.__jinja_wrapper.get_static_file(static_file)
            self.__copy_static_file(static_file_path)

    @staticmethod
    def _get_generator_class(
        render_data_type: RenderDataType,
    ) -> type[RenderInformationGenerator]:
        """
        Returns the specific data generator class that must be used to create the render data of
        the requested type.

        :param render_data_type: Type of the requested render data.
        :returns: The data generator class associated with `render_data_type`.
        """

        if render_data_type is RenderDataType.Summary:
            return SummaryRenderInfoGenerator
        elif render_data_type is RenderDataType.SourceList:
            return SourceListRenderInfoGenerator
        elif render_data_type is RenderDataType.RuleList:
            return RuleListRenderInfoGenerator
        elif render_data_type is RenderDataType.RuleDetails:
            return RuleDetailsRenderInfoGenerator
        elif render_data_type is RenderDataType.Listing:
            return ListingsRenderInfoGenerator
        elif render_data_type is RenderDataType.ViolationList:
            return ViolationListRenderInfoGenerator
        assert_never(render_data_type)

    def __create_report_file_prototype(self) -> ReportFile:
        return ReportFile(
            report_title=self.__report_name,
            ciqar_tag=self._application_tag,
        )

    def __prepare_output_dir(self) -> None:
        # TODO: Check (and warn?) if directory already exists (and is not empty)
        self.__output_path.mkdir(parents=True, exist_ok=True)

    def __generate_template_file(
        self, template_render_information: FileRenderInformation
    ) -> None:
        """
        Generate the file repesented by the provided data.
        """
        rendered_file_content = self.__jinja_wrapper.render_template(
            template_render_information.input_template_name,
            data=template_render_information.template_data,
        )

        self.__write_rendered_file(
            template_render_information.output_file_path, rendered_file_content
        )

    def __write_rendered_file(self, output_file_name: Path, content: str) -> None:
        output_file = self.__output_path.joinpath(output_file_name)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(data=content, encoding="utf8")

    def __copy_static_file(self, static_file_path: Path) -> None:
        shutil.copy(static_file_path, self.__output_path.joinpath(static_file_path.name))
