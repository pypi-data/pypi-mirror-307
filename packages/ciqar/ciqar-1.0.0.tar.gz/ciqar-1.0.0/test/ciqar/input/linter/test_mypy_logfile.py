"""
Unit tests for the mypy_logfile module.
"""

from __future__ import annotations

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem
import pytest

from ciqar.input import Violation
from ciqar.input.linter.mypy_logfile import MypyLogfileParser
from ciqar.input.linter.result_parser import GlobalWarning


class TestMypyLogfileParser:
    """
    Unit tests for the MypyLogfileParser class.
    """

    @pytest.mark.parametrize(
        "logfile_content, expected_violations, expected_global_messages",
        [
            ("", [], []),  # Empty file
            (  # Normal log file
                """
/src/file1.py:37: error: Function is missing a return type annotation  [no-untyped-def]
/src/file2.py:42: error: Need type annotation for "message_type"  [var-annotated]
            """,
                [
                    Violation(
                        filename=Path("/src/file1.py"),
                        linenumber=37,
                        severity="error",
                        rule_id="no-untyped-def",
                        message_text="Function is missing a return type annotation",
                    ),
                    Violation(
                        filename=Path("/src/file2.py"),
                        linenumber=42,
                        severity="error",
                        rule_id="var-annotated",
                        message_text='Need type annotation for "message_type"',
                    ),
                ],
                [],
            ),
            (  # Violation type may be missing sometimes
                """
/src/file.py:411: error: Can use starred expression only as assignment target
            """,
                [
                    Violation(
                        filename=Path("/src/file.py"),
                        linenumber=411,
                        severity="error",
                        rule_id="unknown",
                        message_text="Can use starred expression only as assignment target",
                    ),
                ],
                [],
            ),
            (  # Ignore summary and empty lines
                """
Running MyPy version X.Y.Z...
Generated HTML report (via XSLT): /path/to/mypy/html/report.html

Found 35 errors in 8 files (checked 17 source files)
/src/file.py:42: error: Need type annotation for "message_type"  [var-annotated]
            """,
                [
                    Violation(
                        filename=Path("/src/file.py"),
                        linenumber=42,
                        severity="error",
                        rule_id="var-annotated",
                        message_text='Need type annotation for "message_type"',
                    ),
                ],
                [],
            ),
            (  # "Global" errors do not create a Violation object
                """
/path/to/file.py:64: note: (Skipping most remaining errors due to unresolved imports or missing stubs; fix these first)
mypy.ini: [mypy]: Unrecognized option: enable-error-code = ["ignore-without-code"]
Found 15487 errors in 908 files (errors prevented further checking)
            """,
                [],
                [
                    "Skipping most remaining errors due to unresolved imports or missing stubs; fix these first",
                    'mypy.ini: [mypy]: Unrecognized option: enable-error-code = ["ignore-without-code"]',
                    "Some violations have been skipped: errors prevented further checking",
                ],
            ),
            (  # Merge follow-up notes into a single violation
                """
/src/file1.py:37: error: Function is missing a return type annotation  [no-untyped-def]
/src/file1.py:37: note: Use "-> None" if function does not return a value
/src/file2.py:42: error: Need type annotation for "message_type"  [var-annotated]
/src/file2.py:51: note: This is a separate note not to be merged!
/path/to/file.py:64: note: (Skipping most remaining errors due to unresolved imports or missing stubs; fix these first)
            """,
                [
                    Violation(
                        filename=Path("/src/file1.py"),
                        linenumber=37,
                        severity="error",
                        rule_id="no-untyped-def",
                        message_text='Function is missing a return type annotation\nnote: Use "-> None" if function does not return a value',
                    ),
                    Violation(
                        filename=Path("/src/file2.py"),
                        linenumber=42,
                        severity="error",
                        rule_id="var-annotated",
                        message_text='Need type annotation for "message_type"',
                    ),
                    Violation(
                        filename=Path("/src/file2.py"),
                        linenumber=51,
                        severity="note",
                        rule_id="unknown",
                        message_text="This is a separate note not to be merged!",
                    ),
                ],
                [
                    "Skipping most remaining errors due to unresolved imports or missing stubs; fix these first",
                ],
            ),
            (  # Don't get confused if there are additional [ ] in the message
                """
/src/file1.py:36: error: Incompatible types in assignment (expression has type "Callable[[Any, VarArg(Any), KwArg(Any)], Any]", variable has type "Callable[[BaseType, Any], Any]")  [assignment]
            """,
                [
                    Violation(
                        filename=Path("/src/file1.py"),
                        linenumber=36,
                        severity="error",
                        rule_id="assignment",
                        message_text='Incompatible types in assignment (expression has type "Callable[[Any, VarArg(Any), KwArg(Any)], Any]", variable has type "Callable[[BaseType, Any], Any]")',
                    )
                ],
                [],
            ),
            (  # Don't mixup follow-up notes ending with "]" and real violations on the same line
                """
/src/file2.py:40: error: No overload variant of "get" of "dict" matches argument types "UUID", "Tuple[]"  [call-overload]
/src/file2.py:40: note: Possible overload variants:
/src/file2.py:40: note:     def get(self, _FancyType, /) -> Optional[Tuple[Any, ...]]
/src/file2.py:40: note:     def [_T] get(self, _FancyType, Union[Tuple[Any, ...], _T], /) -> Union[Tuple[Any, ...], _T]
/src/file2.py:40: error: Returning Any from function declared to return "OrdinaryUser"  [no-any-return]
            """,
                [
                    Violation(
                        filename=Path("/src/file2.py"),
                        linenumber=40,
                        severity="error",
                        rule_id="call-overload",
                        message_text=(
                            'No overload variant of "get" of "dict" matches argument types "UUID", "Tuple[]"\n'
                            "note: Possible overload variants:\n"
                            "note:     def get(self, _FancyType, /) -> Optional[Tuple[Any, ...]]\n"
                            "note:     def [_T] get(self, _FancyType, Union[Tuple[Any, ...], _T], /) -> Union[Tuple[Any, ...], _T]"
                        ),
                    ),
                    Violation(
                        filename=Path("/src/file2.py"),
                        linenumber=40,
                        severity="error",
                        rule_id="no-any-return",
                        message_text='Returning Any from function declared to return "OrdinaryUser"',
                    ),
                ],
                [],
            ),
            (  # Special handling for follow-ups that point to a different file and/or line
                """
/src/file3.py:123: error: Unexpected keyword argument "reflect" for "MetaData"  [call-arg]
/usr/lib/python3.7/site-packages/sqlalchemy-stubs/sql/schema.pyi:314: note: "MetaData" defined here
           """,
                [
                    Violation(
                        filename=Path("/src/file3.py"),
                        linenumber=123,
                        severity="error",
                        rule_id="call-arg",
                        message_text=(
                            'Unexpected keyword argument "reflect" for "MetaData"\n'
                            '/usr/lib/python3.7/site-packages/sqlalchemy-stubs/sql/schema.pyi:314: note: "MetaData" defined here'
                        ),
                    )
                ],
                [],
            ),
        ],
    )
    def test_parse_violations(
        self,
        logfile_content: str,
        expected_violations: list[Violation],
        expected_global_messages: list[str],
        fs: FakeFilesystem,
    ) -> None:
        MYPY_LOGFILE = Path("/tmp/mypy.log")

        fs.create_file(MYPY_LOGFILE, contents=logfile_content.strip())
        parser = MypyLogfileParser(result_file=MYPY_LOGFILE, result_base_path=Path("/out"))

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
        assert expected_global_messages == [m.message_text for m in global_messages]

    def test_analyzer_name(self) -> None:
        parser = MypyLogfileParser(result_file=Path("/tmp/result.log"))
        assert parser.analyzer_name == "MyPy"
