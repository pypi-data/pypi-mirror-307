"""
Unit tests for the ciqar.templates.api module

Currently, the API module only contains data classes, there is no functionality to test (yet).
So for now, this is a simple import test to ensure the API module can at least be imported
standalone without errors (and to improve the code coverage).
"""


def test_api_import() -> None:
    from ciqar.templates.api import (
        ReportFile,
        SummaryData,
        FileListRow,
        RuleListRow,
        ViolationListRow,
        SourceLine,
    )

    for t in [ReportFile, SummaryData, FileListRow, RuleListRow, ViolationListRow, SourceLine]:
        assert isinstance(t, type)
