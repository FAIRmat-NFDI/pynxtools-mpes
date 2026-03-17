"""Tests for the NOMAD NORTH tool."""

import pytest

try:
    import nomad  # noqa: F401
except ImportError:
    pytest.skip(
        "Skipping NOMAD NORTH tool tests because nomad-lab is not installed",
        allow_module_level=True,
    )

from pynxtools_mpes.nomad.north_tools.mpes import mpes_north_tool_entry_point


def test_importing_north_tool():
    # this will raise an exception if pydantic model validation fails for the north tool
    assert (
        mpes_north_tool_entry_point.id_url_safe == "pynxtools_mpes_mpes"
        or mpes_north_tool_entry_point.id == "nomad-north-mpes"
    ), "NORTHtool entry point has incorrect id or id_url_safe"
