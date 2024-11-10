"""
Test to ensure that all templates provide proper tempate metadata.
"""

from importlib import import_module

import pytest


@pytest.mark.parametrize(
    "template_name",
    [
        "html_detailed",
        "html_singlepage",
    ],
)
def test_template_metadata(template_name: str) -> None:
    """
    Make sure the template metadata module
     - Can be imported
     - Provides `template_files_specification`
     - Lists at least one file to process
    """

    module_path = f"ciqar.templates.{template_name}"
    metadata_module = import_module(module_path)
    assert metadata_module.template_files_specification
    assert (
        metadata_module.template_files_specification["render_files"]
        or metadata_module.template_files_specification["static_files"]
    )
