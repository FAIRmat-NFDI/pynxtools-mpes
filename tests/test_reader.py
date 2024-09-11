"""
Basic example based test for the stm reader
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
