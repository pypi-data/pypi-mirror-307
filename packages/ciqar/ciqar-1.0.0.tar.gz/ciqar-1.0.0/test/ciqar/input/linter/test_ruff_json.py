"""
Unit tests for the ruff_json module.
"""

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem
import pytest

from ciqar.input import Violation
from ciqar.input.linter.ruff_json import RuffJsonParser
from ciqar.input.linter.result_parser import GlobalWarning


class TestRuffJsonParser:
    """
    Unit tests for the RuffJsonParser class.
    """

    @pytest.mark.parametrize(
        "jsonfile_content, expected_violations",
        [
            ("[]", []),  # Minimal valid JSON file (i.e. no violations)
            (  # Normal violations (one with fix, one without)
                """
[
  {
    "cell": null,
    "code": "F401",
    "end_location": {
      "column": 45,
      "row": 7
    },
    "filename": "/path/to/file1.py",
    "location": {
      "column": 26,
      "row": 7
    },
    "message": "`.sourcefiles.SourceFileCollector` imported but unused",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-import"
  },
  {
    "cell": null,
    "code": "E741",
    "end_location": {
      "column": 81,
      "row": 146
    },
    "filename": "/path/to/file2.py",
    "fix": null,
    "location": {
      "column": 80,
      "row": 146
    },
    "message": "Ambiguous variable name: `l`",
    "noqa_row": 146,
    "url": "https://docs.astral.sh/ruff/rules/ambiguous-variable-name"
  }
]
            """,
                [
                    Violation(
                        filename=Path("/path/to/file1.py"),
                        linenumber=7,
                        severity="issue",
                        rule_id="F401",
                        message_text="`.sourcefiles.SourceFileCollector` imported but unused",
                    ),
                    Violation(
                        filename=Path("/path/to/file2.py"),
                        linenumber=146,
                        severity="issue",
                        rule_id="E741",
                        message_text="Ambiguous variable name: `l`",
                    ),
                ],
            ),
        ],
    )
    def test_parse(
        self, jsonfile_content: str, expected_violations: list[Violation], fs: FakeFilesystem
    ) -> None:
        RUFF_JSON_FILE = Path("/tmp/ruff.json")

        fs.create_file(RUFF_JSON_FILE, contents=jsonfile_content.strip())
        parser = RuffJsonParser(result_file=RUFF_JSON_FILE, result_base_path=Path("/out"))

        messages = list(parser.parse())
        violations = [m for m in messages if isinstance(m, Violation)]
        global_messages = [m for m in messages if isinstance(m, GlobalWarning)]
        assert len(expected_violations) == len(violations)
        for expected, parsed in zip(expected_violations, violations):
            assert str(expected.filename) == str(parsed.filename)
            assert expected.linenumber == parsed.linenumber
            assert expected.severity == parsed.severity
            assert expected.message_text == parsed.message_text
            assert expected.rule_id == parsed.rule_id
        assert not global_messages

    def test_analyzer_name(self) -> None:
        parser = RuffJsonParser(result_file=Path("/tmp/result.json"))
        assert parser.analyzer_name == "ruff"
