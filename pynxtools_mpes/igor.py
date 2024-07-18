"""
Parser for the igor binarywave files from the FHI Phoibos detector
"""

import re
from bisect import insort
from typing import Any, Dict, List

import numpy as np
from igor2 import binarywave
from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader
from pynxtools.dataconverter.readers.utils import parse_yml


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


def sort_key(filename: str, pattern: str = r"[^\/_]+_(\d+)_(\d+).ibw$") -> int:
    r"""
    Returns the sort key based on the second group in the regex pattern.
    Default is to match filenames of the form ..._<scan>_<frame>.ibw.
    Where <frame> is used as the sort key.

    Args:
        filename (str): The filename to return a sort key for.
        pattern (str, optional):
            The sort key pattern. Defaults to r"[^\/_]+_(\d+)_(\d+).ibw$".

    Raises:
        ValueError: If no match in the filename is found.

    Returns:
        int: The sort key.
    """
    groups = re.search(pattern, filename)
    if groups is not None:
        return int(groups.group(2))
    raise ValueError(
        "Invalid filename: Expected file of the form ..._<scan>_<frame>.ibw."
    )


def find_scan_sets(
    filenames: List[str], pattern: str = r"[^\/_]+_(\d+)_(\d+).ibw$"
) -> Dict[int, Any]:
    r"""
    Returns a dict of scan sets where the key is the scan number
    and the value is a list of filenames.
    Default is to match filenames of the form ..._<scan>_<frame>.ibw.
    Where <frame> is used as the sort key and <scan> is used to indicate the scan number.

    Args:
        filenames (List[str]): _description_
        pattern (str, optional): _description_. Defaults to r"[^\/_]+_(\d+)_(\d+).ibw$".

    Returns:
        Dict[int, Any]: _description_
    """
    scan_sets: Dict[int, Any] = {}
    for fn in filenames:
        groups = re.search(pattern, fn)
        if groups is not None:
            scan = int(groups.group(1))
            if scan not in scan_sets:
                scan_sets[scan] = []
            insort(scan_sets[scan], fn, key=lambda fn: sort_key(fn, pattern))
    return scan_sets


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

    supported_nxdls = ["NXmpes", "NXmpes_arpes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ibw_files = []
        self.eln_data = None
        self.ibw_data = {}
        self.scan_nos = []

        self.extensions = {
            ".yml": self.handle_eln_file,
            ".yaml": self.handle_eln_file,
            ".ibw": self.collect_ibw_file,
        }

    def handle_eln_file(self, file_path: str) -> Dict[str, Any]:
        self.eln_data = parse_yml(file_path)
        return {}

    def get_eln_data(self, path: str) -> Any:
        """Returns data from the given eln path."""
        if self.eln_data is None:
            return None

        return self.eln_data.get(path)

    def get_data(self, path: str) -> Dict[str, Any]:
        self.ibw_data.get(f"{self.callbacks.entry_name}/{path}")
        return {}

    def get_entry_names(self) -> List[str]:
        return [f"entry{scan_no}" for scan_no in self.scan_nos]

    def post_process(self) -> None:
        """
        Reads the igor binarywave files and returns a dictionary containing the data.

        Args:
            filenames (List[str]): The filenames to read.

        Returns:
            Dict[str, Any]: The dictionary containing the data.
        """
        for scan_no, files in find_scan_sets(self.ibw_files).items():
            self.scan_nos.append(scan_no)
            waves = []
            beta = []
            theta = []
            for file in files:
                ibw = binarywave.load(file)
                notes = parse_note(ibw["note"])
                beta.append(float(notes["Beta"]))
                theta.append(float(notes["Theta"]))
                waves.append(ibw["wave"]["wData"])

            data_entry = f"entry{scan_no}/data"
            self.ibw_data[f"entry{scan_no}/theta"] = theta
            self.ibw_data[
                f"entry{scan_no}/process/energy_referencing/reference_peak"
            ] = "vacuum level"
            self.ibw_data[f"{data_entry}/@axes"] = ["theta", "beta", "energy"]
            self.ibw_data[f"{data_entry}/beta"] = beta
            self.ibw_data[f"{data_entry}/beta/@units"] = "degrees"
            self.ibw_data[f"{data_entry}/energy"] = axis_from(ibw, 0)
            self.ibw_data[f"{data_entry}/energy/@units"] = axis_units_from(ibw, 0)
            self.ibw_data[f"{data_entry}/theta"] = axis_from(ibw, 1)
            self.ibw_data[f"{data_entry}/theta/@units"] = axis_units_from(ibw, 1)
            self.ibw_data[f"{data_entry}/@signal"] = "data"
            self.ibw_data[f"{data_entry}/data"] = (
                np.array(waves).swapaxes(1, 2).swapaxes(0, 1)
            )
            self.ibw_data[f"{data_entry}/data/@units"] = "counts"
            self.ibw_data[f"{data_entry}/energy/@type"] = "kinetic"

    def collect_ibw_file(self, file_path: str) -> Dict[str, Any]:
        self.ibw_files.append(file_path)
        return {}


READER = IgorReader
