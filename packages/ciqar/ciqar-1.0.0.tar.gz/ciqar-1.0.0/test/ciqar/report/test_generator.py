from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

from pyfakefs.fake_filesystem import FakeFilesystem
import pytest

from ciqar.input.linter.result_parser import LinterResultParser
from ciqar.input.sourcefiles import SourceFileCollector
from ciqar.report.datagen import FileRenderInformation
from ciqar.report.datagen._base import RenderInformationGenerator
from ciqar.report.datagen.listings import ListingsRenderInfoGenerator
from ciqar.report.datagen.rules import (
    RuleListRenderInfoGenerator,
    RuleDetailsRenderInfoGenerator,
)
from ciqar.report.datagen.sources import SourceListRenderInfoGenerator
from ciqar.report.datagen.summary import SummaryRenderInfoGenerator
from ciqar.report.datagen.violations import ViolationListRenderInfoGenerator
from ciqar.report.generator import ReportGenerator, TemplateMetadata
from ciqar.report.jinja_wrapper import JinjaWrapper
from ciqar.templates.api import RenderDataType, ReportFile


class TestReportGenerator:
    """
    Unit test suite for the ReportGenerator class.
    """

    @pytest.mark.parametrize(
        "render_data_type, expected_generator_class",
        [
            (RenderDataType.Summary, SummaryRenderInfoGenerator),
            (RenderDataType.SourceList, SourceListRenderInfoGenerator),
            (RenderDataType.Listing, ListingsRenderInfoGenerator),
            (RenderDataType.RuleList, RuleListRenderInfoGenerator),
            (RenderDataType.RuleDetails, RuleDetailsRenderInfoGenerator),
            (RenderDataType.ViolationList, ViolationListRenderInfoGenerator),
        ],
    )
    def test__get_generator_class(
        self,
        render_data_type: RenderDataType,
        expected_generator_class: type[RenderInformationGenerator],
    ) -> None:
        """
        Ensures the correct assignment of render data generators to the enum value from the
        template metadata. This is tested separately because the `_get_generator_class()` method
        is patched in other tests to inject a mocked data generator.
        """

        generator_class = ReportGenerator._get_generator_class(render_data_type)
        assert expected_generator_class == generator_class

    @patch("ciqar.report.generator.LinterResultCollector", autospec=True)
    @patch("ciqar.report.generator.JinjaWrapper", autospec=True)
    @pytest.mark.parametrize(
        "render_file_names, static_file_names",
        [
            (["index.html.in"], ["static.txt"]),  # Single file opf each type
            (  # Multiple files of each type
                ["file1.html.in", "file2.html.in"],
                ["static1.txt", "static2.css"],
            ),
            (  # No static files
                ["file1.html.in", "file2.html.in"],
                [],
            ),
            (  # No files to render (strange use case, though)
                [],
                ["static1.txt", "static2.css"],
            ),
            ([], []),  # Nothing to do at all (is there really a use case for this???)
        ],
    )
    def test_generate_report(
        self,
        mocked_jinja_wrapper_cls: Mock,
        _mocked_linter_results_cls: Mock,
        render_file_names: list[str],
        static_file_names: list[str],
        fs: FakeFilesystem,
    ) -> None:
        TEMPLATE_PATH = Path("/input")
        REPORT_OUTPUT_PATH = Path("/report")

        # Create all static files to copy
        static_file_paths = [
            TEMPLATE_PATH.joinpath(file_name) for file_name in static_file_names
        ]
        for file_path in static_file_paths:
            fs.create_file(file_path, contents="STATIC")

        # Setup the JinjaWrapper mock
        mocked_jinja_wrapper = Mock(spec=JinjaWrapper)
        mocked_jinja_wrapper.render_template.return_value = "RENDERED"
        mocked_jinja_wrapper_cls.return_value = mocked_jinja_wrapper
        mocked_jinja_wrapper.get_static_file.side_effect = static_file_paths

        # Create the ReportGenerator instance
        template_metadata = TemplateMetadata(
            template_name="Test Mockup Template",
            render_metadata={
                "render_files": {
                    # DataType is mocked away later, so it doesn't matter which one is set here
                    render_file: RenderDataType.Summary
                    for render_file in render_file_names
                },
                "static_files": static_file_names,
            },
        )

        generator = ReportGenerator(
            source_collector=Mock(spec=SourceFileCollector),
            violations_parser=Mock(spec=LinterResultParser),
            template_metadata=template_metadata,
            output_path=REPORT_OUTPUT_PATH,
            application_tag="Unit test",
        )

        # Setup and inject a mocked render info generator (which the ReportGenerator delegates
        # to), because they are tested separately
        def create_render_info_generator_mock(render_file_name: str) -> Mock:
            render_info_generator_mock = Mock(spec=RenderInformationGenerator)
            render_info_generator_mock.__iter__ = lambda _s: iter(
                [
                    FileRenderInformation(
                        input_template_name=render_file_name,
                        output_file_path=REPORT_OUTPUT_PATH.joinpath(render_file_name[:-3]),
                        template_data=ReportFile(
                            report_title="Unit test example report",
                            ciqar_tag="Unit testing",
                            path_to_report_root="",
                        ),
                    )
                ]
            )
            return render_info_generator_mock

        generator._get_generator_class = Mock(  # type: ignore[method-assign]
            side_effect=[
                Mock(return_value=create_render_info_generator_mock(render_file_name))
                for render_file_name in render_file_names
            ]
        )

        # Execute the test
        generator.generate_report()

        # Check file rendering results
        expected_rendered_files = (
            REPORT_OUTPUT_PATH.joinpath(file_name[:-3]) for file_name in render_file_names
        )
        for rendered_file in expected_rendered_files:
            assert rendered_file.exists()
            assert rendered_file.read_text() == "RENDERED"
        assert mocked_jinja_wrapper.render_template.call_count == len(render_file_names)

        # Check static file processing results
        expected_static_files = [
            REPORT_OUTPUT_PATH.joinpath(file_name) for file_name in static_file_names
        ]
        for static_file in expected_static_files:
            assert static_file.exists()
            assert static_file.read_text() == "STATIC"
        assert mocked_jinja_wrapper.get_static_file.call_count == len(static_file_names)
