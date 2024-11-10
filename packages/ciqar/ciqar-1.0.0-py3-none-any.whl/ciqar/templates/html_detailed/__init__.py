"""
Template definition for the detailed HTML report (which is the default report):
 - Summary page
 - List of all source files
 - List of all rules
 - Rule details
 - Source listings
"""

from ciqar.templates.api import RenderDataType, TemplateFilesDescription


template_files_specification: TemplateFilesDescription = {
    "render_files": {
        "index.html.in": RenderDataType.Summary,
        "source_list.html.in": RenderDataType.SourceList,
        "listing.html.in": RenderDataType.Listing,
        "rule_list.html.in": RenderDataType.RuleList,
        "rule_details.html.in": RenderDataType.RuleDetails,
    },
    "static_files": ["style.css"],
}
