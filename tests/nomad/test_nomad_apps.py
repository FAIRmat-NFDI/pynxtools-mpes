#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Tests for the NOMAD app."""

import pytest

try:
    import nomad  # noqa: F401
except ImportError:
    pytest.skip(
        "Skipping NOMAD app tests because nomad-lab is not installed",
        allow_module_level=True,
    )

# this will raise an exception if pydantic model validation fails for the app
from pynxtools_mpes.nomad.apps import mpes_app, schema  # noqa: PLC0415


def test_mpes_app_basic_properties():
    """Verify basic metadata of the MPES app."""
    app = mpes_app.app

    assert app.label == "MPES"
    assert app.path == "mpesapp"
    assert app.category == "Experiment"


def test_mpes_app_v2_schema():
    """App v2 must reference the correct Mpes class."""
    assert schema == "pynxtools.nomad.metainfo.applications.Mpes"
    filters = mpes_app.app.filters_locked
    assert "section_defs.definition_qualified_name" in filters
    assert filters["section_defs.definition_qualified_name"] == [schema]


def test_mpes_app_locked_filters():
    """Ensure required locked filters are defined and well-formed."""
    app = mpes_app.app

    assert "section_defs.definition_qualified_name" in app.filters_locked
    assert isinstance(
        app.filters_locked["section_defs.definition_qualified_name"], list
    )
    assert len(app.filters_locked["section_defs.definition_qualified_name"]) == 1


def test_mpes_app_columns():
    """Check that a representative result column is configured correctly."""
    app = mpes_app.app

    definition_column = next(col for col in app.columns if col.title == "Definition")
    assert definition_column.selected is True
    assert "data.definition" in definition_column.search_quantity


def test_mpes_app_menu_contains_probe_beam_section():
    """Validate presence and structure of the Elements menu section."""
    app = mpes_app.app

    elements_menu = next(item for item in app.menu.items if item.title == "Probe Beam")

    assert elements_menu.size.name == "LG"
    assert any(item.title == "Probe Source" for item in elements_menu.items)


def test_mpes_app_dashboard_widgets():
    """Ensure the dashboard contains a valid periodic table widget."""
    dashboard = mpes_app.app.dashboard

    assert len(dashboard.widgets) > 0

    histogram = next(w for w in dashboard.widgets if w.type == "histogram")
    assert histogram.layout
    assert histogram.n_bins == 30
    assert (
        histogram.x.search_quantity
        == "data.sample.temperature_env.value#pynxtools.nomad.metainfo.applications.Mpes#float"
    )
