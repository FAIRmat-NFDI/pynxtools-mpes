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
"""Test for NOMAD examples in reader plugins."""

import pytest

try:
    from nomad.parsing.parser import ArchiveParser
    from nomad.datamodel import EntryArchive, Context
except ImportError:
    pytest.skip(
        "Skipping NOMAD example tests because nomad is not installed",
        allow_module_level=True,
    )

from pynxtools.testing.nomad_example import get_file_parameter, test_nomad_example


@pytest.mark.parametrize(
    "mainfile", get_file_parameter("../src/pynxtools_mpes/nomad/examples")
)
def test_nomad_examples(mainfile, no_warn):
    """Test if NOMAD examples work."""
    test_nomad_example(mainfile)


@pytest.mark.parametrize(
    "config, expected_local_path",
    [
        pytest.param(
            {
                "title": "mpes_example",
                "description": "mpes_example",
                "category": "test",
                "path": "nomad/examples",
            },
            f"examples/data/uploads/mpes.zip",
            id="mpes_example",
        ),
    ],
)
def test_nomad_example_upload_entry_point_valid(config, expected_local_path):
    test_example_upload_entry_point_valid(
        plugin_package="pynxtools-mpes",
        config=config,
        expected_local_path=expected_local_path,
    )