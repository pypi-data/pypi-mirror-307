from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence
from typing_extensions import assert_never

from ciqar.input import Violation
from ciqar.input.linter.result_parser import GlobalWarning, LinterResultParser


class LinterResultCollector:
    """
    Collects and provides all linter results from the selected parser.
    """

    # TODO (refactoring): The analyzer name should be provided by the parse() method, the same
    # was all other information is delivered.

    def __init__(
        self, result_parser: LinterResultParser, excluded_source_files: Sequence[Path]
    ):
        """
        :param result_parser: The parser to load result data from.
        """

        self.__analyzer_name = result_parser.analyzer_name

        # self.__result_parser is set to None after loading all results to display the "results
        # available" state (because the data dicts may stay empty if there are no violations at
        # all).
        self.__result_parser: Optional[LinterResultParser] = result_parser
        self.__excluded_source_files = excluded_source_files
        self.__global_messages: list[str] = []

        self.__message_index: dict[Path, dict[int, list[Violation]]] = {}
        self.__message_to_files_index: dict[str, dict[Path, list[int]]] = {}

    def get_analyzer_name(self) -> str:
        """
        Returns the name of the code analyzer that created the read result file.

        :returns: Name of the used code analyzer.
        """

        return self.__analyzer_name

    def get_global_messages(self) -> list[str]:
        """
        Returns a list of linter messages that are not tied to a certain source location (e.g.
        general warnings or errors).

        :return: List of global linter messages.
        """

        self.__load_linter_result_data()
        return self.__global_messages

    def get_all_violations(self) -> list[Violation]:
        """
        Returns the list of all violations found in the requested result file.

        :returns: List of all violations
        """

        self.__load_linter_result_data()
        all_violations = []
        for violations_of_file in self.__message_index.values():
            for violation_list in violations_of_file.values():
                all_violations.extend(violation_list)
        return all_violations

    def __load_linter_result_data(self) -> None:
        if self.__result_parser is None:
            return

        for linter_message in self.__result_parser.parse():
            if isinstance(linter_message, Violation):
                if linter_message.filename in self.__excluded_source_files:
                    # Also ignore all violations from this file.
                    # TODO: Maybe it would be of interest to see which excluded files had been
                    #       analyzed?
                    continue

                self.__message_index.setdefault(linter_message.filename, {}).setdefault(
                    linter_message.linenumber, []
                ).append(linter_message)
                if linter_message.rule_id:
                    self.__message_to_files_index.setdefault(
                        linter_message.rule_id, {}
                    ).setdefault(linter_message.filename, []).append(linter_message.linenumber)
            elif isinstance(linter_message, GlobalWarning):
                self.__global_messages.append(linter_message.message_text)
            else:
                assert_never(linter_message)
        self.__result_parser = None
