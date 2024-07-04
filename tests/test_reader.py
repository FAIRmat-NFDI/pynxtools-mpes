"""
Basic example based test for the stm reader
"""

import os
from pathlib import Path

import pynxtools.dataconverter.convert as dataconverter
from pynxtools.testing.nexus_conversion import ReaderTest


def test_nexus_conversion(caplog, tmp_path):
    """
    Tests the conversion into nexus.
    """
    caplog.clear()
    dir_path = Path(__file__).parent / "data"
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


def test_eln_data(tmp_path):
    """Check if the subsections in the eln_data.yml file work."""
    dir_path = Path(__file__).parent / "data"
    dataconverter.convert(
        (
            str(dir_path / "xarray_saved_small_calibration.h5"),
            str(dir_path / "config_file.json"),
            str(dir_path / "eln_data.yaml"),
        ),
        "mpes",
        "NXmpes",
        os.path.join(tmp_path, "mpes.small_test.nxs"),
        False,
        False,
    )
