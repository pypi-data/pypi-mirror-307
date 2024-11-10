"""
This is the API for report templates. It contains the data types for describing a template as
well as the data structures that are provided to the template files when rendering.

1. Template metadata
Each template must declare which files shall be processed and how. This is done by defining some
metadata, see `TemplateFilesDescription` for further information.

2. Render data
When being rendered, each single template file has access to a `ReportFile` instance which
provides all necessary data. The available data can be different for each file and is specified
by the metadata. See `ReportFile` for further information.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing_extensions import TypedDict


class RenderDataType(Enum):
    """
    Defines how a certain template file must be rendered and which data will be provided.
    """

    Summary = "summary"
    """
    Renders the file once, providing `SummaryData` as `ReportFile.summary_data`. The output file
    is created in the report base directory.
    """

    ViolationList = "violations"
    """
    Renders the file once, providing a list of `ViolationListRow`s as
    `ReportFile.violation_list_data`. The output file is created in the report base directory.
    """

    SourceList = "sources"
    """
    Renders the file once, providing a list of `FileListRow`s as `ReportFile.file_list_data`.
    The output file is created in the report base directory.
    """

    RuleList = "rule_list"
    """
    Renders the file once, providing a list of `RuleListRow`s as `ReportFile.rule_list_data`.
    The output file is created in the report base directory.
    """

    RuleDetails = "rule_details"
    """
    Renders the file multiple times (once for each rule occuring in the linter result),
    providing a list of `FileListRow`s as `ReportFile.file_list_data`. The output files are
    created within the "rules" directory of the report and use the corresponding rule name as
    file name.
    """

    Listing = "listing"
    """
    Renders the file multiple times (once for each source file), providing a list of
    `SourceLine`s as `ReportFile.source_content_data`. The output files are created within the
    "sources" directory of the report and replicate the original source tree and filenames.
    """


class TemplateFilesDescription(TypedDict):
    """
    Description of the files to be processed for a certain template.
    For all files within the template directory, this `dict` specifies whether they should be
    copied as they are (`static_files`) or rendered with some data (`render_files`). Existing
    files that are not mentioned in this `dict` are ignored. Here, "file" always means the
    complete file name (including a ".in" suffix) but without any paths.

    The `render_files` component is a `dict` which assigns one of the `RenderDataType` enum
    values to each file, specifying how to render it and which data must be provided. Note that
    files can be rendered multiple times with different data (producing different output files),
    also depending on the `RenderDataType` See there for further information.

    The `static_files` component is a simple `list` of files that should be copied without any
    modifications (no rendering). They end up in the root of the report output directory.

    This is a `TypedDict` to avoid unnecessary boiler plate in the template description, so
    regular `dict` syntax must be used for the metadata definition.

    Example usage:
    ```
    template_metadata: TemplateFilesDescription = {
        "render_files": {
            "index.html.in": RenderDataType.Summary,
        },
        "static_files": ["style.css"],
    }
    ```
    """

    render_files: dict[str, RenderDataType]
    """ Definition of files that needs to be rendered (and how). """

    static_files: list[str]
    """ Files to copy as they are (not modifications). """


@dataclass
class ReportFile:
    """
    Provides all data needed to render a single file of the report.

    Besides the basic data, a ReportFile instance usually contains additional data specific to
    the template file being rendered (e.g. a template file for a "Summary" page will have the
    optional `summary_data` property set to some useful data). Which data is provided for which
    file is defined by the template metadata, see `TemplateFilesDescription` for further
    information.
    """

    report_title: str
    """ Title of the whole report (e.g. "MyPy check report"). """

    ciqar_tag: str
    """ Ciqar name and version used for report generation. """

    path_to_report_root: str = ""
    """ Relative path from the current file to the report root, "" if the file is in root. """

    context_name: str = ""
    """
    Display name of the context object which may be displayed e.g. as part of the page title.
    For example, the context can be the file to be shown or the linter rule to show
    files/violations of. In these cases, `context_name` would be the file name or the rule name
    respectively. May be empty if there is no special context.
    """

    summary_data: SummaryData | None = None
    """ Report summary data, if `RenderDataType.Summary` is requested by the metadata. """

    rule_list_data: list[RuleListRow] | None = None
    """ Rule list data, if `RenderDataType.RuleList` is requested by the metadata. """

    file_list_data: list[FileListRow] | None = None
    """
    File list data, if  either`RenderDataType.SourceList` or `RenderDataType.RuleDetails` are
    requested by the metadata.
    """

    source_content_data: list[SourceLine] | None = None
    """ Data for a source listing, if `RenderDataType.Listing` is requested by the metadata. """

    violation_list_data: list[ViolationListRow] | None = None
    """ Violation list data, if `RenderDataType.ViolationList` is requested by the metadata. """


@dataclass
class SummaryData:
    """
    Provides all data needed for a short report summarization.
    """

    source_file_count: int
    """ Total number of found source files. """

    violation_count: int
    """ Total number of violations. """

    line_count: int
    """ Total number of source lines. """

    bad_line_count: int
    """ Total number of bad source lines. """

    generation_time: str
    """ Date and time of the report generation, formatted suitable for displaying. """

    analyzer_tag: str
    """ Displayable analyzer name tag, e.g. a linter's name + version. """

    global_linter_messages: list[str]
    """
    Linter messages that are not assigned to a certain source code line (e.g. warning messages).
    """


@dataclass
class RuleListRow:
    """
    Provides the data of a single row in a list of rules.
    "Rule" is the linter option/check/rule that causes a certain violation. Usually, rules can
    be enabled or disabled in the linter settings. The exact denomination varies between
    different linters, but Ciqar uses the term "rule".
    """

    rule_name: str
    """ Name/ID of the linter rule. """

    violation_count: int
    """ Number of violations caused by this rule. """

    example_message: str
    """
    Example message for supporting the user in understanding the rules.
    This is simply one of the found messages.
    """


@dataclass
class FileListRow:
    """
    Provides the data of a single row in a list of source files.
    """

    display_filename: str
    """ File path and name as shown in the report. """

    report_filename: str
    """ File path to the destination file in the report (relative to the report root). """

    line_count: int
    """ Number of code lines in this file (empty lines do not count). """

    bad_line_count: int
    """ Number of lines that caused at least one violation. """

    violation_count: int
    """ Number of violations caused by this file. """

    rating: int
    """ Rating of this file based on the report result: 0 = "good" to 2 = "bad". """
    # TODO: Maybe there is a better rating than just numbers? I.e. "good", "bad", "?"?


@dataclass
class SourceLine:
    """
    Provides all data of a single line in a source code file.
    """

    lineno: int
    """ Line number. """

    content: str
    """ Line content. """

    rating: str
    """ Rating of this line based on the report result: "good", "empty", "bad". """

    messages: list[str]
    """ List of all Violation messages caused by this line. """


@dataclass
class ViolationListRow:
    """
    Provides the data of a single row in a list of violations.
    """

    display_filename: str
    """ File path and name as shown in the report. """

    lineno: int
    """ Line number """

    rule: str
    """ Linter rule that enables/disables this violation. """

    message_lines: list[str]
    """
    Message text of this violation, one line per list item.
    There is always at least one line. Storing multiline messages as list of strings allows the
    template to easily control the handling of line breaks (e.g. "\n" vs. "<br/>").
    """
