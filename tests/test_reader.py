"""
Basic example based test for the stm reader
"""

import logging
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pynxtools.dataconverter.convert as dataconverter
from pynxtools.dataconverter.convert import get_reader
from pynxtools.dataconverter.helpers import generate_template_from_nxdl
from pynxtools.dataconverter.template import Template
from pynxtools.dataconverter.validation import validate_dict_against
from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nexus_definitions_path
from pynxtools.nexus.nexus import HandleNexus

from pynxtools_mpes.reader import MPESReader


def test_example_data(caplog):
    """
    Test the example data for the stm reader
    """
    reader = MPESReader
    assert callable(reader.read)

    def_dir = get_nexus_definitions_path()

    data_dir = Path(__file__).parent / "data"
    input_files = (
        str(data_dir / "config_file.json"),
        str(data_dir / "xarray_saved_small_calibration.h5"),
    )

    nxdl_file = os.path.join(def_dir, "contributed_definitions", "NXmpes.nxdl.xml")

    root = ET.parse(nxdl_file).getroot()
    template = Template()
    generate_template_from_nxdl(root, template)

    read_data = reader().read(template=Template(template), file_paths=input_files)

    assert isinstance(read_data, Template)
    with caplog.at_level(logging.WARNING):
        assert validate_dict_against("NXmpes", read_data)

    # Ensure there were no warning logs
    assert not caplog.text


def test_mpes_writing(tmp_path):
    """Check if mpes example can be reproduced"""
    # dataconverter
    dir_path = Path(__file__).parent / "data"
    dataconverter.convert(
        (
            str(dir_path / "xarray_saved_small_calibration.h5"),
            str(dir_path / "config_file.json"),
        ),
        "mpes",
        "NXmpes",
        os.path.join(tmp_path, "mpes.small_test.nxs"),
        False,
        False,
    )
    # check generated nexus file
    test_data = os.path.join(tmp_path, "mpes.small_test.nxs")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(tmp_path, "mpes_test.log"), "w")
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = HandleNexus(logger, test_data, None, None)
    nexus_helper.process_nexus_master_file(None)
    with open(
        os.path.join(tmp_path, "mpes_test.log"), "r", encoding="utf-8"
    ) as logfile:
        log = logfile.readlines()
    with open(dir_path / "Ref_nexus_mpes.log", "r", encoding="utf-8") as logfile:
        ref_log = logfile.readlines()
    assert log == ref_log


def test_shows_correct_warnings():
    """
    Checks whether the read function generates the correct warnings.
    """
    def_dir = get_nexus_definitions_path()

    data_dir = Path(__file__).parent / "data"
    input_files = (
        str(data_dir / "config_file.json"),
        str(data_dir / "xarray_saved_small_calibration.h5"),
    )
    nxdl_file = os.path.join(def_dir, "contributed_definitions", "NXmpes.nxdl.xml")

    root = ET.parse(nxdl_file).getroot()
    template = Template()
    generate_template_from_nxdl(root, template)

    read_data = get_reader("mpes")().read(
        template=Template(template), file_paths=tuple(input_files)
    )

    assert validate_dict_against("NXmpes", read_data)


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
