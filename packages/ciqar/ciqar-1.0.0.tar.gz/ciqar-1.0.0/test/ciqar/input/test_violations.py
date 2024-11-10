"""
Unit tests for the ciqar.input.violations module.
"""

from __future__ import annotations

from pathlib import Path
from typing import cast
from unittest.mock import Mock

import pytest

from ciqar.input import Violation
from ciqar.input.linter.result_parser import (
    ParsedMessageType,
    LinterResultParser,
    GlobalWarning,
)
from ciqar.input.violations import LinterResultCollector


def _create_dummy_violation(message: str, filename: str | None = None) -> Violation:
    return Violation(
        filename=Path(filename if filename else "/file.py"),
        linenumber=27,
        severity="error",
        message_text=message,
        rule_id="unit test",
    )


def test_get_analyzer_name() -> None:
    """
    Tests the correct forwarding of the analyzer's name.
    """

    result_parser = TestLinterResultCollector.create_result_parser([])

    collector = LinterResultCollector(result_parser=result_parser, excluded_source_files=[])

    assert collector.get_analyzer_name() == result_parser.analyzer_name


@pytest.mark.parametrize(
    "parsed_messages, excluded_files",
    [
        ([], []),
        ([GlobalWarning(message_text="Global Message")], []),
        ([_create_dummy_violation("Test Mock Message")], []),
        (
            [
                GlobalWarning(message_text="Global Message"),
                _create_dummy_violation("Test Mock Message"),
            ],
            [],
        ),
        (
            [
                GlobalWarning(message_text="Global Message 1"),
                _create_dummy_violation("Test Mock Message 1"),
                GlobalWarning(message_text="Global Message 2"),
                _create_dummy_violation("Test Mock Message 2"),
            ],
            [],
        ),
        (
            [
                GlobalWarning(message_text="Global Message 1"),
                _create_dummy_violation("Test Mock Message 1", filename="/file1.py"),
                _create_dummy_violation("Test Mock Message 2", filename="/file2.py"),
            ],
            ["/file1.py"],
        ),
    ],
)
class TestLinterResultCollector:
    """
    Unit test suite for the LinterResultCollector class.
    The common test function paarmeters are:
    :param parsed_messages:
    :param excluded_files:
    """

    @staticmethod
    def create_result_parser(parsed_messages: list[ParsedMessageType]) -> LinterResultParser:
        result_parser = Mock(spec=LinterResultParser)
        result_parser.parse = Mock(return_value=iter(parsed_messages))
        result_parser.analyzer_name = "Unit Test Mockup"
        return result_parser

    def test_get_global_messages(
        self, parsed_messages: list[ParsedMessageType], excluded_files: list[str]
    ) -> None:
        """
        Tests the correct behaviour of the get_global_messages() method:
         - Provide all global messages
         - The first call must parse all data
         - A second call must return the same data, but without parsing again
        """

        result_parser = self.create_result_parser(parsed_messages)
        expected_global_messages = [
            pm.message_text for pm in parsed_messages if isinstance(pm, GlobalWarning)
        ]

        collector = LinterResultCollector(
            result_parser=result_parser,
            excluded_source_files=[Path(ef) for ef in excluded_files],
        )

        global_messages = collector.get_global_messages()
        assert global_messages == expected_global_messages
        cast(Mock, result_parser.parse).assert_called_once()

        # Query a second time, there must be no additional parsing!
        global_messages = collector.get_global_messages()
        assert global_messages == expected_global_messages
        cast(Mock, result_parser.parse).assert_called_once()

    def test_get_all_violations(
        self, parsed_messages: list[ParsedMessageType], excluded_files: list[str]
    ) -> None:
        """
        Tests the correct behaviour of the get_all_violations() method.
         - Provide all violations
         - The first call must parse all data
         - A second call must return the same data, but without parsing again
        """

        result_parser = self.create_result_parser(parsed_messages)
        expected_violations = [
            pm
            for pm in parsed_messages
            if isinstance(pm, Violation) and str(pm.filename) not in excluded_files
        ]

        collector = LinterResultCollector(
            result_parser=result_parser,
            excluded_source_files=[Path(ef) for ef in excluded_files],
        )

        violations = collector.get_all_violations()
        assert violations == expected_violations
        cast(Mock, result_parser.parse).assert_called_once()

        # Query a second time, there must be no additional parsing!
        violations = collector.get_all_violations()
        assert violations == expected_violations
        cast(Mock, result_parser.parse).assert_called_once()
