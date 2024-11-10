"""
Template definition for the one-page HTML report, which is basically a list of violations
"""

from ciqar.templates.api import RenderDataType, TemplateFilesDescription


template_files_specification: TemplateFilesDescription = {
    "render_files": {
        "index.html.in": RenderDataType.ViolationList,
    },
    "static_files": [],
}
