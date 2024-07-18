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
"""
Basic example based test for the MPES reader
"""

from pathlib import Path

from pynxtools.testing.nexus_conversion import ReaderTest


def test_nexus_conversion(caplog, tmp_path):
    """
    Tests the conversion into nexus.
    """
    caplog.clear()
    dir_path = Path(__file__).parent / "data" / "mpes"
    test = ReaderTest(
        nxdl="NXmpes",
        reader_name="mpes",
        files_or_dir=[
            str(dir_path / "xarray_saved_small_calibration.h5"),
            str(dir_path / "config_file.json"),
            str(dir_path / "example.nxs"),
        ],
        tmp_path=tmp_path,
        caplog=caplog,
    )
    test.convert_to_nexus(caplog_level="WARNING", ignore_undocumented=False)
    test.check_reproducibility_of_nexus()


def test_conversion_w_eln_data(caplog, tmp_path):
    """
    Tests the conversion with additional ELN data
    """
    caplog.clear()
    dir_path = Path(__file__).parent / "data" / "mpes"
    test = ReaderTest(
        nxdl="NXmpes",
        reader_name="mpes",
        files_or_dir=[
            str(dir_path / "xarray_saved_small_calibration.h5"),
            str(dir_path / "config_file.json"),
            str(dir_path / "eln_data.yaml"),
            str(dir_path / "example_eln.nxs"),
        ],
        tmp_path=tmp_path,
        caplog=caplog,
    )
    test.convert_to_nexus(caplog_level="WARNING", ignore_undocumented=False)
    test.check_reproducibility_of_nexus()
