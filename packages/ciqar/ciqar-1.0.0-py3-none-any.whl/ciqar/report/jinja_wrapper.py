from __future__ import annotations

from pathlib import Path
from typing import cast

from jinja2 import Environment, PackageLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound, TemplateError


class JinjaWrapper:
    """
    Represents the Jinja2 library.
    All Jinja2 dependent code is wrapped in this class, to decouple the dependency from
    the application and make mocking as well as future updates easier.
    """

    def __init__(self, template_package_name: str):
        self._jinja_environment = Environment(
            loader=PackageLoader(
                package_name="ciqar.templates", package_path=template_package_name
            ),
            autoescape=select_autoescape(
                enabled_extensions=("html", "in"),
                default_for_string=True,
            ),
        )

    def render_template(self, template_filename: str, **report_data: object) -> str:
        try:
            template = self._jinja_environment.get_template(template_filename)
        except TemplateNotFound:
            # Casting is safe because we explicitly provide PackageLoader to the Jinja
            # environment during __init()__.
            raise FileNotFoundError(
                "Requested template '{0}' not found in package '{1}'.".format(
                    template_filename,
                    cast(PackageLoader, self._jinja_environment.loader).package_path,
                )
            )

        try:
            return template.render(**report_data)
        except TemplateError as e:
            # Wrap Jinja2 exception types
            raise TemplateRenderError(str(e))

    def get_static_file(self, template_filename: str) -> Path:
        """
        Returns the absolute path of the requested template file.
        This is useful for files that simply need to be copied (without any Jinja processing).

        :param template_filename: Name of a file within the current template.
        :returns: Absolute path of the requested file.
        :raises FileNotFoundError: The requested file does not exist in the template.
        """

        # Create the "not found" error message in case it is needed later. Casting is safe
        # because we explicitly provided PackageLoader to the Jinja environment during
        # __init()__.
        error_message = "Requested static file '{0}' not found in package '{1}'.".format(
            template_filename, cast(PackageLoader, self._jinja_environment.loader).package_path
        )
        try:
            template = self._jinja_environment.get_template(template_filename)
        except TemplateNotFound:
            raise FileNotFoundError(error_message)

        if not template.filename:
            raise FileNotFoundError(error_message)

        return Path(template.filename)


class TemplateRenderError(Exception):
    """
    Raised on error rendering an existing template. This usually wraps a Jinja2 exception and
    contains the original error message.
    Errors may be caused e.g. by invalid template syntax or missing/incomplete context data.
    """
