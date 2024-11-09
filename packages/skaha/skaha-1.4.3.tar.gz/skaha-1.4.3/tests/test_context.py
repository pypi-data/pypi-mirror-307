"""Test Skaha Context API."""

import pytest

from skaha.context import Context


@pytest.fixture(scope="session")
def context():
    """Test Context."""
    context = Context()
    yield context
    del context


def test_context(context):
    """Test context fetch."""
    assert "defaultCores" in context.resources()
