"""
Unit tests for the `ciqar.application` module.
"""

from __future__ import annotations

from argparse import ArgumentParser, ArgumentTypeError
from functools import partial
from pathlib import Path
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

from ciqar.application import CiqarApplication
from ciqar.input.linter.mypy_logfile import MypyLogfileParser
from ciqar.input.linter.pyright_json import PyrightJsonParser
from ciqar.input.linter.ruff_json import RuffJsonParser
from ciqar.input.linter.result_parser import LinterResultParser
from ciqar.report.generator import ReportGenerator


# TODO: It'd be cool to have a test for the command line interface, i.e. allowed options and
# their syntax, to get a warning when the CLI changes. But I don't have a good idea of how to
# do this, yet.
def _create_argparse_mock(mocked_argparser_cls: Mock) -> None:
    argument_parser_mock = Mock(spec=ArgumentParser)
    argument_parser_mock.parse_args = MagicMock()
    argument_parser_mock.parse_args.return_value.template_metadata = ("default", {})
    mocked_argparser_cls.return_value = argument_parser_mock


@patch("ciqar.application.ArgumentParser")
def test_app_description(argument_parser_cls_mock: Mock) -> None:
    """
    Simple tests for the application name and version properties.
    """

    _create_argparse_mock(argument_parser_cls_mock)

    application = CiqarApplication()
    assert application.application_name == "Ciqar"

    version_strings = application.application_version.split(".")
    assert len(version_strings) == 3
    major, minor, bug = version_strings
    assert major.isdigit()
    assert minor.isdigit()
    assert bug.isdigit()


@pytest.mark.parametrize(
    "result_url, expected_factory_class, expected_result_path",
    [
        ("mypy:/path/to/file.log", MypyLogfileParser, Path("/path/to/file.log")),
        ("pyright:/path/to/file.json", PyrightJsonParser, Path("/path/to/file.json")),
        ("ruff:/path/to/file.json", RuffJsonParser, Path("/path/to/file.json")),
    ],
)
def test__parse_analyzer_result_url__normal_usecase(
    result_url: str,
    expected_factory_class: type[LinterResultParser],
    expected_result_path: Path,
) -> None:
    """
    Tests parsing of analyzer result URLs (as provided on command line).
    """
    parser_factory = CiqarApplication._parse_analyzer_result_url(analyzer_result_url=result_url)
    expected_factory = partial(expected_factory_class, expected_result_path)

    # Returning a "partial" object is not a requirement to test, but the following three checks
    # rely on it. So we want a warning if this ever chanegs, because then we need to adapt this
    # test case as well.
    assert isinstance(
        parser_factory, partial
    ), "The test requries the factory to be a 'partial' object"
    assert parser_factory.func == expected_factory.func
    assert parser_factory.args == expected_factory.args
    assert parser_factory.keywords == expected_factory.keywords


@pytest.mark.parametrize(
    "invalid_result_url",
    [
        "unknown:/some/file.bin",  # Unknown analyzer
        "/missing/url/scheme.txt",  # Invalid URL - Scheme is missing
        "mypy:",  # Invalid URL: Path is missing
    ],
)
def test__parse_analyzer_result_url__errorcases(invalid_result_url: str) -> None:
    """
    Tests the behaviour when the provided result URL is invalid.
    """
    with pytest.raises(ArgumentTypeError):
        CiqarApplication._parse_analyzer_result_url(analyzer_result_url=invalid_result_url)


def test__load_template_files_specification() -> None:
    """
    Tests loading of template metadata by a name (as provided on command line).
    """

    # Test case 1: Load a valid, existing template (the default one)
    template_name, template_files_spec = CiqarApplication._load_template_files_specification(
        template_name="html_detailed"
    )
    assert template_name == "html_detailed"
    assert len(template_files_spec["static_files"]) > 0
    assert len(template_files_spec["render_files"]) > 0

    # Test case 2: Requested template does not exist
    with pytest.raises(ArgumentTypeError):
        CiqarApplication._load_template_files_specification(template_name="does_not_exist")

    # Test case 3: Requested template exists as module, but doesn't provide the necessary
    # metadata
    # Pretend the metadata module has been imported already, and set it to something not
    # providing the desired metadata
    sys.modules["ciqar.templates.invalid_template"] = sys
    with pytest.raises(ArgumentTypeError):
        CiqarApplication._load_template_files_specification(template_name="invalid_template")
    del sys.modules["ciqar.templates.invalid_template"]


@patch("ciqar.application.ArgumentParser")
@patch("ciqar.application.ReportGenerator")
@patch("ciqar.application.SourceFileCollector")
def test_run(
    _source_collector_cls_mock: Mock,
    generator_cls_mock: Mock,
    argument_parser_cls_mock: Mock,
) -> None:
    """
    Simple test case for the run() method. Makes sure the ReportGenerator is run).
    """

    _create_argparse_mock(argument_parser_cls_mock)
    generator_mock = Mock(spec=ReportGenerator)
    generator_cls_mock.return_value = generator_mock

    app = CiqarApplication()
    app.run()

    assert generator_mock.generate_report.call_count == 1
