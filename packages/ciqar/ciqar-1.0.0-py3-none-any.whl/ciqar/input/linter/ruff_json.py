"""
Definition of the RuffJsonParser class.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator
from typing_extensions import override

from ciqar.input import Violation
from ciqar.input.linter.result_parser import LinterResultParser, ParsedMessageType


class RuffJsonParser(LinterResultParser):
    """
    Parser implementation for extracting violations from a ruff JSON result file.
    """

    @property
    @override
    def analyzer_name(self) -> str:
        return "ruff"

    @override
    def parse(self) -> Iterator[ParsedMessageType]:
        json_data = json.load(self._result_file.open("rt"))
        for violation_data in json_data:
            violation = Violation(
                filename=Path(violation_data["filename"]),
                linenumber=violation_data["location"]["row"],
                severity="issue",
                message_text=violation_data["message"],
                rule_id=violation_data.get("code"),
            )
            yield violation
