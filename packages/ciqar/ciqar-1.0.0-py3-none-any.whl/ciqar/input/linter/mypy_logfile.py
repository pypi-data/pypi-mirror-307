"""
Definition of the MypyLogfileParser class.
"""

from __future__ import annotations

import re
from typing import Iterator
from typing_extensions import override

from ciqar.input import Violation
from ciqar.input.linter.result_parser import (
    GlobalWarning,
    LinterResultParser,
    ParsedMessageType,
)


class MypyLogfileParser(LinterResultParser):
    """
    Parser implementation for extracting violations from a MyPy logfile.
    """

    @property
    @override
    def analyzer_name(self) -> str:
        return "MyPy"

    @override
    def parse(self) -> Iterator[ParsedMessageType]:
        current_violation = None

        with self._result_file.open("rt") as fh:
            for log_line in fh:
                log_line = log_line.strip()

                # Ignore empty lines
                if not log_line:
                    continue

                # Is it a global message?
                global_message = self.__parse_global_message(log_line)
                if global_message:
                    # No need to merge into any previous message, so yield it now
                    if current_violation:
                        yield current_violation
                        current_violation = None
                    yield GlobalWarning(message_text=global_message)
                    continue

                # Is it a regular violation message?
                violation = self.__parse_violation(log_line)
                if violation is not None:
                    if (
                        current_violation
                        and violation.filename == current_violation.filename
                        and violation.linenumber == current_violation.linenumber
                        and violation.severity == "note"
                        and violation.rule_id == "unknown"
                    ):
                        # Merge into previous violation
                        current_violation.message_text = "{0}\n{1}: {2}".format(
                            current_violation.message_text,
                            violation.severity,
                            violation.message_text,
                        )
                    elif (
                        current_violation
                        and "defined here" in violation.message_text
                        and violation.severity == "note"
                        and violation.rule_id == "unknown"
                    ):
                        # Merge into previous violation
                        current_violation.message_text = "{0}\n{1}".format(
                            current_violation.message_text, log_line
                        )
                    else:
                        # This is another violation, so do not merge!
                        if current_violation:
                            yield current_violation
                            current_violation = None
                        current_violation = violation
                # else: Parse error, ignore this line

            # Yield the last violation, if any
            if current_violation:
                yield current_violation
                current_violation = None

    def __parse_violation(self, line: str) -> Violation | None:
        parts = re.fullmatch(
            r"(?P<filepath>.+?)"
            r":(?P<lineno>\d+)"
            r":(?:\d+:)?\s(?P<severity>\w+)"
            r":\s(?P<message>.+)"
            r"\s+\[(?P<rule>[a-z\-]+)\]$",
            line,
        )
        if not parts:
            parts = re.fullmatch(
                r"(?P<filepath>.+?)"
                r":(?P<lineno>\d+)"
                r":(?:\d+:)?\s(?P<severity>\w+)"
                r":\s(?P<message>.+)",
                line,
            )
            if not parts:
                return None
            rule = "unknown"
        else:
            rule = parts["rule"]

        filename = parts["filepath"]
        severity = parts["severity"]
        lineno = int(parts["lineno"].strip())
        text = parts["message"].rstrip()

        return Violation(
            filename=self._result_base_path.joinpath(filename),
            linenumber=lineno,
            severity=severity,
            message_text=text,
            rule_id=rule,
        )

    def __parse_global_message(self, line: str) -> str | None:
        message = ""

        summary_message_regexp = re.compile(
            r"^Found \d+ errors in \d+ files \(checked \d+ source files\)$"
        )
        if summary_message_regexp.match(line):
            # Ignore the usual check summary
            return None
        elif "Unrecognized option:" in line:
            # Warning about invalid MyPy config option
            message = line
        else:
            groups: re.Match[str] | None = re.fullmatch(r".+\((?P<message>.+)\)", line)
            if groups is None:
                return None

            if line.startswith("Found") and "errors prevented further checking" in line:
                message = "Some violations have been skipped: {}".format(groups["message"])
            elif "Skipping most remaining errors" in line:
                message = groups["message"]

        return message
