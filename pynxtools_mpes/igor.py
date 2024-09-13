"""
Parser for the igor binarywave files from the FHI Phoibos detector
"""

import logging
import re
from typing import Any, Dict, List, Optional

import numpy as np
from igor2 import binarywave
from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader
from pynxtools.dataconverter.readers.utils import parse_yml

logger = logging.getLogger("pynxtools")

def parse_note(bnote: bytes) -> Dict[str, Any]:
    """
    Parsers the note field of the igor binarywave file.
    It assumes that the note field contains key-value pairs of the
    form 'key=value' separated by newlines.

    Args:
        bnote (bytes): The bytes of the binarywave note field.

    Returns:
        Dict[str, Any]: The dictionary of the parsed note field.
    """
    note = bnote.decode("utf-8").replace("\r", "\n")
    notes = {}
    for line in note.split():
        split = line.split("=")
        if len(split) == 2:
            key, val = split
            notes[key] = val

    return notes


def axis_from(ibw_data: Dict[str, Any], dim: int) -> np.ndarray:
    """
    Returns the axis values for a given dimension from the wave header.

    Args:
        ibw_data (Dict[str, Any]): The ibw data containing the wave_header.
        dim (int): The dimension to return the axis for.

    Returns:
        np.ndarray: The axis values.
    """
    wave_header = ibw_data["wave"]["wave_header"]
    return (
        wave_header["sfA"][dim] * np.arange(wave_header["nDim"][dim])
        + wave_header["sfB"][dim]
    )


def axis_units_from(ibw_data: Dict[str, Any], dim: int) -> str:
    """ "
    Returns the unit for a given dimension from the wave header.

    Args:
        ibw_data (Dict[str, Any]): The ibw data containing the wave_header.
        dim (int): The dimension to return the unit for.

    Returns:
        str: The axis units
    """
    unit_arr = ibw_data["wave"]["wave_header"]["dimUnits"][dim]

    unit = ""
    for elem in unit_arr:
        unit += elem.decode("utf-8")

    return unit


class IgorReader(MultiFormatReader):
    """Reader for FHI specific igor binarywave files"""

    supported_nxdls = ["NXmpes", "NXmpes_arpes", "NXxrd"]
    config_file: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ibw_files = []
        self.eln_data = None
        self.ibw_data = {}
        self.ibw_attrs = {}
        self.scan_nos = []

        self.extensions = {
            ".yml": self.handle_eln_file,
            ".yaml": self.handle_eln_file,
            ".json": self.set_config_file,
            ".ibw": self.collect_ibw_file,
        }

    def handle_eln_file(self, file_path: str) -> Dict[str, Any]:
        self.eln_data = parse_yml(file_path)
        return {}

    def get_eln_data(self, key: str, path: str) -> Any:
        """Returns data from the given eln path."""
        if self.eln_data is None:
            return None

        return self.eln_data.get(path)

    def set_config_file(self, file_path: str) -> Dict[str, Any]:
        if self.config_file is not None:
            logger.info(f"Config file already set. Skipping the new file {file_path}.")
        self.config_file = file_path
        return {}

    def get_data(self, key: str, path: str) -> Any:
        return self.ibw_data.get(path)

    def get_attr(self, key: str, path: str) -> Any:
        return self.ibw_attrs.get(path)

    def post_process(self) -> None:
        for file in self.ibw_files:
            ibw = binarywave.load(file)
            self.ibw_attrs = parse_note(ibw["wave"]["note"])
            for dim in range(ibw["wave"]['wave_header']["nDim"].size):
                self.ibw_data[f"axis{dim}"] = axis_from(ibw, dim)
                self.ibw_data[f"axis{dim}/@units"] = axis_units_from(ibw, dim)
            self.ibw_data["data"] = ibw["wave"]["wData"]
            self.ibw_data["data/@units"] = ibw["wave"]["data_units"]

    def collect_ibw_file(self, file_path: str) -> Dict[str, Any]:
        self.ibw_files.append(file_path)
        return {}


READER = IgorReader
