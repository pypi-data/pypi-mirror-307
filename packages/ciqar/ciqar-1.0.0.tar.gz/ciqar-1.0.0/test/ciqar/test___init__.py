"""
Unit tests for the `ciqar.__init__` module
"""

from __future__ import annotations

from unittest.mock import Mock, patch

from ciqar import main
from ciqar.application import CiqarApplication


@patch("ciqar.application.CiqarApplication")
def test_main(mocked_application_cls: Mock) -> None:
    """Should simply startup the application."""

    mocked_application = Mock(spec=CiqarApplication)
    mocked_application_cls.return_value = mocked_application

    main()

    assert mocked_application_cls.call_count == 1
    assert mocked_application.run.call_count == 1
