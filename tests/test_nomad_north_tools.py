"""Tests for the NOMAD NORTH tool."""

from importlib.metadata import entry_points

import pytest

try:
    import nomad  # noqa: F401
except ImportError:
    pytest.skip(
        "Skipping NOMAD NORTH tool tests because nomad-lab is not installed",
        allow_module_level=True,
    )

from pynxtools_mpes.nomad.north_tools import mpes, mpes_north_tool


def test_north_tool_entry_point_registered():
    # exercises the actual mechanism NOMAD uses to discover the tool at runtime
    # (pyproject.toml's [project.entry-points.'nomad.plugin']), not just a direct import
    (entry_point,) = entry_points(group="nomad.plugin", name="mpes_north_tool")
    assert entry_point.load() is mpes


def test_north_tool_id_url_safe():
    # this will raise an exception if pydantic model validation fails for the north tool
    assert mpes.id_url_safe == "mpes", "NORTHTool entry point has incorrect id_url_safe"


def test_north_tool_image_reference():
    # regression test: catches an unrendered cookiecutter placeholder or a stale/incorrect
    # image path, either of which would silently fail to pull at container-launch time
    assert mpes_north_tool.image == "ghcr.io/fairmat-nfdi/pynxtools-mpes:main"


def test_north_tool_metadata():
    assert mpes_north_tool.display_name == "mpes"
    assert {"nxs", "h5", "hdf5"} <= set(mpes_north_tool.file_extensions)
    assert mpes_north_tool.default_url == "/desktop"
    assert mpes_north_tool.maintainer, "NORTHTool must list at least one maintainer"
