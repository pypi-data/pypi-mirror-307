"""
Unit test suites for the ciqar.report.datagen package
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator
from unittest.mock import Mock

import pytest

from ciqar.input import SourceFile, Violation
from ciqar.report.datagen import RenderInformationGeneratorConfig
from ciqar.report.datagen.listings import ListingsRenderInfoGenerator
from ciqar.report.datagen.rules import (
    RuleDetailsRenderInfoGenerator,
    RuleListRenderInfoGenerator,
)
from ciqar.report.datagen.sources import SourceListRenderInfoGenerator
from ciqar.report.datagen.summary import SummaryRenderInfoGenerator
from ciqar.report.datagen.violations import ViolationListRenderInfoGenerator
from ciqar.templates.api import ReportFile, ViolationListRow


@pytest.fixture
def report_file_prototype() -> Iterator[ReportFile]:
    yield ReportFile(report_title="Unit test report", ciqar_tag="Ciqar Test")


class _RenderInfoGeneratorTestSuite:
    _source_root_path = Path("/src")

    _output_base_dir = Path("/out")

    @staticmethod
    def _create_source_file_mock(file_path: Path, file_contents: list[str]) -> SourceFile:
        mocked_source_file = Mock(spec=SourceFile)
        mocked_source_file.absolute_path = file_path
        mocked_source_file.project_relative_path = file_path.relative_to(
            _RenderInfoGeneratorTestSuite._source_root_path
        )
        mocked_source_file.line_count = len(file_contents)
        mocked_source_file.content = file_contents
        return mocked_source_file

    @staticmethod
    def _create_dummy_violations(violations: list[tuple[str, int]]) -> list[Violation]:
        """
        Tuple items of violations: File path, line number
        """

        return [
            Violation(
                filename=Path(filepath),
                linenumber=lineno,
                severity="test",
                message_text="Fake message: {}:{}".format(filepath, lineno),
                rule_id="unit test",
            )
            for filepath, lineno in violations
        ]

    def _create_dummy_violation(
        self, filepath: Path, lineno: int, rule_name: str, message: str
    ) -> Violation:
        return Violation(
            filename=filepath,
            linenumber=lineno,
            rule_id=rule_name,
            message_text=message,
            severity="error",
        )


class TestSummaryRenderInfoGenerator(_RenderInfoGeneratorTestSuite):
    @pytest.mark.parametrize(
        "source_files, violations, global_messages",
        [
            (dict(), [], []),  # No data given at all
            (dict(), [], ["Error message 1", "Warning message 2"]),  # Global messages
            ({"/src/file.py": 0}, [], []),  # Empty file
            ({"/src/file1.py": 27, "/src/file2.py": 53}, [], []),  # Multiple files with content
            ({"/src/dir1/file1.py": 1, "/src/dir2/file2.py": 2}, [], []),  # Subdirectories
            (  # Some violations
                {"/src/file1.py": 32, "/src/file2.py": 64},
                [("/src/file1.py", 15)],
                [],
            ),
            (  # Multiple violations within the same line
                {"/src/file1.py": 10},
                [("/src/file1.py", 4), ("/src/file1.py", 4), ("/src/file1.py", 6)],
                [],
            ),
        ],
    )
    def test_summary(
        self,
        source_files: dict[str, int],
        violations: list[tuple[str, int]],
        global_messages: list[str],
        report_file_prototype: ReportFile,
    ) -> None:
        """
        Note: source_files must only be empty if violations is empty, too!
        """

        analyzer_name = "Ciqar Unit Test"
        factory = SummaryRenderInfoGenerator(
            generator_config=RenderInformationGeneratorConfig(
                report_base_path=self._output_base_dir,
                report_file_prototype=report_file_prototype,
                source_files=[
                    self._create_source_file_mock(Path(p), [str(i) for i in range(c)])
                    for p, c in source_files.items()
                ],
                violations=self._create_dummy_violations(violations),
                input_template_name="summary.html.in",
                global_messages=global_messages,
                analyzer_name=analyzer_name,
            )
        )

        render_information_list = list(factory)

        # There must be exactly one summary file
        assert len(render_information_list) == 1

        render_info = render_information_list[0]
        assert render_info.input_template_name == "summary.html.in"
        assert render_info.output_file_path == self._output_base_dir.joinpath("summary.html")
        assert render_info.template_data.path_to_report_root == ""
        assert render_info.template_data.context_name == ""
        assert render_info.template_data.summary_data is not None
        assert render_info.template_data.rule_list_data is None
        assert render_info.template_data.file_list_data is None
        assert render_info.template_data.source_content_data is None
        assert render_info.template_data.violation_list_data is None

        summary_data = render_info.template_data.summary_data
        assert summary_data.analyzer_tag == analyzer_name
        assert summary_data.global_linter_messages == global_messages
        assert summary_data.source_file_count == len(source_files)
        assert summary_data.line_count == sum(source_files.values())
        assert summary_data.violation_count == len(violations)
        assert summary_data.bad_line_count == len({"{}:{}".format(f, l) for f, l in violations})
        assert summary_data.generation_time != ""  # Make sure there is at least something


class TestListingsRenderInfoGenerator(_RenderInfoGeneratorTestSuite):
    @pytest.mark.parametrize(
        "source_files, violations",
        [
            (dict(), []),  # No files given at all
            ({"/src/file1.py": ["line1", "line2"]}, []),  # Single file with several lines
            (  # Several files
                {
                    "/src/file1.py": ["line1"],
                    "/src/file2.py": ["line2"],
                },
                [],
            ),
            (  # Subdirectories
                {
                    "/src/dir1/file1.py": ["line1"],
                    "/src/dir2/file2.py": ["line2"],
                },
                [],
            ),
            ({"/src/file1.py": []}, []),  # Empty file
            (  # File with a violation
                {"/src/file1.py": ["line1", "line2"]},
                [("/src/file1.py", 1)],
            ),
            (  # Several files with violations
                {
                    "/src/file1.py": ["line1", "line2"],
                    "/src/dir/file2.py": ["line1", "line2", "line3"],
                },
                [
                    ("/src/file1.py", 1),
                    ("/src/file1.py", 2),
                    ("/src/dir/file2.py", 2),
                ],
            ),
        ],
    )
    def test_render_data_generation(
        self,
        source_files: dict[str, list[str]],
        violations: list[tuple[str, int]],
        report_file_prototype: ReportFile,
    ) -> None:
        factory = ListingsRenderInfoGenerator(
            generator_config=RenderInformationGeneratorConfig(
                report_base_path=self._output_base_dir,
                report_file_prototype=report_file_prototype,
                source_files=[
                    self._create_source_file_mock(Path(p), c) for p, c in source_files.items()
                ],
                violations=self._create_dummy_violations(violations),
                input_template_name="source_listing.html.in",
                global_messages=[],
                analyzer_name="",
            )
        )

        render_information_list = list(factory)
        files_to_bad_linenumbers: dict[str, list[int]] = {}
        for f, l in violations:
            files_to_bad_linenumbers.setdefault(f, []).append(l)

        assert len(render_information_list) == len(source_files)
        for (source_file_path, expected_file_content), render_info in zip(
            source_files.items(), render_information_list
        ):
            project_relative_sourcefile_path = Path(source_file_path).relative_to(
                self._source_root_path
            )
            expected_output_path = self._output_base_dir.joinpath(
                "sources",
                Path(source_file_path).with_suffix(".html").relative_to(self._source_root_path),
            )
            expected_report_root_url = "../" * (
                len(project_relative_sourcefile_path.parts[:-1]) + 1
            )
            assert render_info.input_template_name == "source_listing.html.in"
            assert render_info.output_file_path == expected_output_path
            assert render_info.template_data.path_to_report_root == expected_report_root_url
            assert render_info.template_data.context_name == str(
                project_relative_sourcefile_path
            )
            assert render_info.template_data.summary_data is None
            assert render_info.template_data.rule_list_data is None
            assert render_info.template_data.file_list_data is None
            assert render_info.template_data.source_content_data is not None
            assert render_info.template_data.violation_list_data is None

            source_content = render_info.template_data.source_content_data

            # Correct line count?
            assert len(source_content) == len(expected_file_content)
            # Correct line numbers?
            assert [l.lineno for l in source_content] == list(
                range(1, len(expected_file_content) + 1)
            )
            # Correct line content?
            assert [l.content for l in source_content] == expected_file_content
            # Correct violation messages?
            assert all(
                not l.messages
                for l in source_content
                if l.lineno not in files_to_bad_linenumbers.get(source_file_path, [])
            )
            assert all(
                l.messages == ["test: Fake message: {}:{}".format(source_file_path, l.lineno)]
                for l in source_content
                if l.lineno in files_to_bad_linenumbers.get(source_file_path, [])
            )
            # Correct line ratings?
            assert all(
                l.rating == "good"
                for l in source_content
                if l.lineno not in files_to_bad_linenumbers.get(source_file_path, [])
            )
            assert all(
                l.rating == "bad"
                for l in source_content
                if l.lineno in files_to_bad_linenumbers.get(source_file_path, [])
            )


class TestSourceListRenderInfoGenerator(_RenderInfoGeneratorTestSuite):
    @pytest.mark.parametrize(
        "source_files",
        [
            dict(),  # No files given at all
            {"/src/file.py": 3},  # Single file
            {"/src/file.py": 0},  # Empty file
            {  # Multiple files in subdirectories
                "/src/file0.py": 7,
                "/src/dir1/file1.py": 42,
                "/src/dir2/file2.py": 13,
            },
        ],
    )
    def test_source_file_collection(
        self, source_files: dict[str, int], report_file_prototype: ReportFile
    ) -> None:
        factory = SourceListRenderInfoGenerator(
            generator_config=RenderInformationGeneratorConfig(
                report_base_path=self._output_base_dir,
                report_file_prototype=report_file_prototype,
                source_files=[
                    self._create_source_file_mock(Path(p), [str(i) for i in range(c)])
                    for p, c in source_files.items()
                ],
                violations=[],
                input_template_name="view_by_file.html.in",
                global_messages=[],
                analyzer_name="",
            )
        )

        render_information_list = list(factory)

        # There must be exactly one file to render
        assert len(render_information_list) == 1

        render_info = render_information_list[0]
        assert render_info.input_template_name == "view_by_file.html.in"
        assert render_info.output_file_path == self._output_base_dir.joinpath(
            "view_by_file.html"
        )
        assert render_info.template_data.path_to_report_root == ""
        assert render_info.template_data.context_name == ""
        assert render_info.template_data.summary_data is None
        assert render_info.template_data.rule_list_data is None
        assert render_info.template_data.file_list_data is not None
        assert render_info.template_data.source_content_data is None
        assert render_info.template_data.violation_list_data is None

        file_list = render_info.template_data.file_list_data
        assert len(file_list) == len(source_files)

        project_relative_sourcefile_paths = [
            Path(f).relative_to(self._source_root_path) for f in source_files.keys()
        ]

        expected_output_paths = sorted(
            [
                str(Path("sources").joinpath(f).with_suffix(".html"))
                for f in project_relative_sourcefile_paths
            ]
        )
        # Correct source listing paths?
        assert sorted([f.report_filename for f in file_list]) == expected_output_paths
        # Correct display names?
        source_root_len = len(str(self._source_root_path))
        expected_display_names = sorted(f[source_root_len + 1 :] for f in source_files.keys())
        assert sorted([f.display_filename for f in file_list]) == expected_display_names
        # Correct line counts?
        assert all(
            f.line_count
            == source_files[str(self._source_root_path.joinpath(f.display_filename))]
            for f in file_list
        )
        # There must be no violations
        assert all(f.violation_count == 0 for f in file_list)
        # There must be no bad lines
        assert all(f.bad_line_count == 0 for f in file_list)
        # All ratings umst be "good"
        assert all(f.rating == 0 for f in file_list)


class TestRuleListRenderInfoGenerator(_RenderInfoGeneratorTestSuite):
    @pytest.mark.parametrize(
        "violation_tuples_by_rules",
        [
            {},  # No violations given at all
            {
                "rule1": [
                    ("/src/file.py", 3, "message1"),
                ]
            },  # Single rule
            {  # Multiple rules within multiple files
                "rule1": [
                    ("/src/file1.py", 3, "message1"),
                    ("/src/file2.py", 5, "message2"),
                ],
                "rule2": [
                    ("/src/file2.py", 2, "message3"),
                ],
            },
        ],
    )
    def test_rule_list_view_generation(
        self,
        violation_tuples_by_rules: dict[str, list[tuple[str, int, str]]],
        report_file_prototype: ReportFile,
    ) -> None:
        expected_violations_by_rules = {
            rule: [
                self._create_dummy_violation(
                    filepath=Path(f), lineno=l, rule_name=rule, message=m
                )
                for f, l, m in violation_list
            ]
            for rule, violation_list in violation_tuples_by_rules.items()
        }
        violation_list = [v for vl in expected_violations_by_rules.values() for v in vl]

        factory = RuleListRenderInfoGenerator(
            generator_config=RenderInformationGeneratorConfig(
                report_base_path=self._output_base_dir,
                report_file_prototype=report_file_prototype,
                source_files=[],
                violations=violation_list,
                input_template_name="view_by_rule.html.in",
                global_messages=[],
                analyzer_name="",
            ),
        )

        render_information_list = list(factory)

        # There must be exactly one rule list view
        assert len(render_information_list) == 1

        render_info = render_information_list[0]

        # Rule names
        assert render_info.input_template_name == "view_by_rule.html.in"
        assert render_info.output_file_path == self._output_base_dir.joinpath(
            "view_by_rule.html"
        )
        assert render_info.template_data.context_name == ""
        assert render_info.template_data.path_to_report_root == ""
        assert render_info.template_data.summary_data is None
        assert render_info.template_data.rule_list_data is not None
        assert render_info.template_data.file_list_data is None
        assert render_info.template_data.source_content_data is None
        assert render_info.template_data.violation_list_data is None

        rule_list = render_info.template_data.rule_list_data

        # Correct rule names?
        assert sorted([rule.rule_name for rule in rule_list]) == sorted(
            expected_violations_by_rules.keys()
        )

        # Correct violation counts?
        assert all(
            rule.violation_count == len(expected_violations_by_rules[rule.rule_name])
            for rule in rule_list
        )

        # Correct example messages?
        assert all(
            rule.example_message == expected_violations_by_rules[rule.rule_name][0].message_text
            for rule in rule_list
        )


class TestRuleDetailsRenderInfoGenerator(_RenderInfoGeneratorTestSuite):
    @pytest.mark.parametrize(
        "violation_tuples_by_rules",
        [
            {},  # No violations given at all
            {"rule1": [("/src/file.py", 3, "message1")]},  # Single rule
            {  # Multiple rules within multiple files
                "rule1": [
                    ("/src/file1.py", 3, "message1"),
                    ("/src/file2.py", 5, "message2"),
                ],
                "rule2": [
                    ("/src/file2.py", 2, "message3"),
                ],
            },
        ],
    )
    def test_rule_details_generation(
        self,
        violation_tuples_by_rules: dict[str, list[tuple[str, int, str]]],
        report_file_prototype: ReportFile,
    ) -> None:
        expected_line_counts_of_files: dict[Path, int] = {}
        for filename, new_linecount, _m in [
            item for sublist in violation_tuples_by_rules.values() for item in sublist
        ]:
            filepath = Path(filename)
            line_count = expected_line_counts_of_files.setdefault(filepath, 0)
            if new_linecount > line_count:
                expected_line_counts_of_files[filepath] = new_linecount

        expected_violations_by_rules: dict[str, list[Violation]] = {
            rule: [
                self._create_dummy_violation(
                    filepath=Path(f), lineno=l, rule_name=rule, message=m
                )
                for f, l, m in violation_list
            ]
            for rule, violation_list in violation_tuples_by_rules.items()
        }
        violation_list = [v for vl in expected_violations_by_rules.values() for v in vl]

        source_file_mocks = [
            self._create_source_file_mock(f, [str(i) for i in range(l)])
            for f, l in expected_line_counts_of_files.items()
        ]

        factory = RuleDetailsRenderInfoGenerator(
            generator_config=RenderInformationGeneratorConfig(
                report_base_path=self._output_base_dir,
                report_file_prototype=report_file_prototype,
                source_files=source_file_mocks,
                violations=violation_list,
                input_template_name="view_files_of_rule.html.in",
                global_messages=[],
                analyzer_name="",
            ),
        )

        render_information_list = list(factory)

        # Correct number of rules?
        assert len(render_information_list) == len(expected_violations_by_rules)

        # Each rule must be returned only once
        seen_rules: list[str] = []
        for render_info in render_information_list:
            assert render_info.input_template_name == "view_files_of_rule.html.in"
            assert render_info.output_file_path == self._output_base_dir.joinpath(
                "rules", "{}.html".format(render_info.template_data.context_name)
            )

            assert render_info.template_data.context_name
            assert render_info.template_data.context_name not in seen_rules
            seen_rules.append(render_info.template_data.context_name)
            assert render_info.template_data.context_name in expected_violations_by_rules

            assert render_info.template_data.path_to_report_root == "../"
            assert render_info.template_data.summary_data is None
            assert render_info.template_data.rule_list_data is None
            assert render_info.template_data.file_list_data is not None
            assert render_info.template_data.source_content_data is None
            assert render_info.template_data.violation_list_data is None

            expected_violation_data = expected_violations_by_rules[
                render_info.template_data.context_name
            ]
            project_relative_sourcefile_paths = [
                v.filename.relative_to(self._source_root_path) for v in expected_violation_data
            ]
            expected_output_paths = sorted(
                [
                    str(Path("sources").joinpath(f).with_suffix(".html"))
                    for f in project_relative_sourcefile_paths
                ]
            )

            file_list = render_info.template_data.file_list_data

            # Correct source file count?
            assert len(file_list) == len(project_relative_sourcefile_paths)

            # Correct source listing paths?
            assert sorted(f.report_filename for f in file_list) == expected_output_paths
            # Correct display names?
            expected_display_names = sorted(str(f) for f in project_relative_sourcefile_paths)
            assert sorted({f.display_filename for f in file_list}) == expected_display_names
            # Correct violation counts?
            assert all(
                f.violation_count
                == sum(
                    [
                        1
                        for v in expected_violation_data
                        if v.filename == self._source_root_path.joinpath(f.display_filename)
                    ]
                )
                for f in file_list
            )

            # Correct line counts?
            bad_lines_in_bad_files: dict[Path, list[int]] = {}
            for v in expected_violation_data:
                bad_lines_in_bad_files.setdefault(v.filename, []).append(v.linenumber)

            ## Bad lines
            assert all(
                f.bad_line_count
                == len(
                    bad_lines_in_bad_files[self._source_root_path.joinpath(f.display_filename)]
                )
                for f in file_list
            )

            ## Total lines
            assert all(
                (
                    expected_line_counts_of_files[
                        self._source_root_path.joinpath(f.display_filename)
                    ]
                    == f.line_count
                )
                for f in file_list
            )

            # Rating
            # For now: Must never be "good" since all files have violations
            assert all(f.rating > 0 for f in file_list)


class TestViolationListRenderInfoGenerator(_RenderInfoGeneratorTestSuite):
    @pytest.mark.parametrize(
        "violations",
        [
            [],  # No violations given at all
            [("/src/file.py", 3)],  # Single violation
            [  # Multiple violations sperad over multiple files
                ("/src/file1.py", 3),
                ("/src/file1.py", 10),
                ("/src/file2.py", 7),
            ],
            [  # Test correct sorting
                ("/src/bbb.py", 5),
                ("/src/aaa.py", 4),
                ("/src/aaa.py", 1),
                ("/src/bbb.py", 8),
            ],
        ],
    )
    def test_rule_list_view_generation(
        self,
        violations: list[tuple[str, int]],
        report_file_prototype: ReportFile,
    ) -> None:
        input_violation_list = self._create_dummy_violations(violations)
        input_source_files = [
            self._create_source_file_mock(file_path=Path(path), file_contents=[])
            for path, _line in violations
        ]

        factory = ViolationListRenderInfoGenerator(
            generator_config=RenderInformationGeneratorConfig(
                report_base_path=self._output_base_dir,
                report_file_prototype=report_file_prototype,
                source_files=input_source_files,
                violations=input_violation_list,
                input_template_name="violation_list.html.in",
                global_messages=[],
                analyzer_name="",
            ),
        )

        render_information_list = list(factory)

        expected_violation_rows = [
            ViolationListRow(
                display_filename=str(v.filename.relative_to(self._source_root_path)),
                lineno=v.linenumber,
                rule=v.rule_id,
                message_lines=v.message_text.split("\n"),
            )
            for v in input_violation_list
        ]
        expected_violation_rows = sorted(
            expected_violation_rows, key=lambda v: (v.display_filename, v.lineno)
        )

        # There must be exactly one rule list view
        assert len(render_information_list) == 1

        render_info = render_information_list[0]

        assert render_info.input_template_name == "violation_list.html.in"
        assert render_info.output_file_path == self._output_base_dir.joinpath(
            "violation_list.html"
        )
        assert render_info.template_data.context_name == ""
        assert render_info.template_data.path_to_report_root == ""
        assert render_info.template_data.summary_data is None
        assert render_info.template_data.rule_list_data is None
        assert render_info.template_data.file_list_data is None
        assert render_info.template_data.source_content_data is None
        assert render_info.template_data.violation_list_data is not None

        violation_list = render_info.template_data.violation_list_data
        assert len(violation_list) == len(violations)
        assert expected_violation_rows == violation_list
