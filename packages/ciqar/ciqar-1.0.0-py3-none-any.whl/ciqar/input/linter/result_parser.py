from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional, Union

from ciqar.input import Violation


@dataclass
class GlobalWarning:
    """
    Represents a linter message that is not tied to a certain source location (e.g. general
    warnings or errors).
    """

    message_text: str
    """ The message text. """


ParsedMessageType = Union[Violation, GlobalWarning]
""" A parsed message that is provided by the parser. """


class LinterResultParser(ABC):
    """
    Base class for all result parser implementations.
    Represents a parser providing all reported violations one by one.
    """

    def __init__(self, result_file: Path, result_base_path: Optional[Path] = None):
        """
        :param result_file: Linter result file to read violation information from.
        :param result_base_path: The absolute path any relative paths in the linter result file
                                 are relative to.
        """

        self._result_file = result_file
        self._result_base_path = (
            result_base_path if result_base_path else self._result_file.parent.resolve()
        )

    @property
    @abstractmethod
    def analyzer_name(self) -> str:
        """
        Name of the code analyzer that created the result file processed by this parser.
        """

    @abstractmethod
    def parse(self) -> Iterator[ParsedMessageType]:
        """
        Parses the result data into single messages and returns them one by one.
        """
