"""
Data types containing all input data.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional


class SourceFile:
    """
    Represents a single source file. This is the data type provided by SourceFileCollector.
    """

    def __init__(self, absolute_path: Path, project_base_path: Path):
        """
        :raises: The provided file does not exit
        """
        if not absolute_path.exists():
            raise FileNotFoundError("File not found: {}".format(absolute_path))

        self.absolute_path = absolute_path
        self.project_relative_path = absolute_path.relative_to(project_base_path)
        self._line_count: Optional[int] = None

    @property
    def line_count(self) -> int:
        """
        Returns the number of non-empty lines in this file.
        Line containing only whitespace are considered "empty".
        """
        if self._line_count is None:
            self._line_count = sum(
                1 for line in self.absolute_path.open("rt").readlines() if line.strip()
            )
        return self._line_count

    @property
    def content(self) -> Iterator[str]:
        with self.absolute_path.open("rt") as fh:
            for line in fh:
                yield line.rstrip()


@dataclass
class Violation:
    """
    Represents a single violation from the linter result. This is the data type provided
    by LinterResultCollector.
    """

    filename: Path
    """
    Full path to the source file this violation was reported in.
    """

    linenumber: int
    """
    Line number this violation was reported for.
    """

    severity: str  # TODO: What about using an enum for the severity?
    message_text: str  # TODO: Refactor to a list of string (multiline messages)
    rule_id: str
    """
    The rule ID/name as reported by the linter (e.g. "E123" or "unused-import").
    """
