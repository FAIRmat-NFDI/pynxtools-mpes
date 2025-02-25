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
"""MPES reader implementation for the DataConverter."""

import logging
from functools import reduce
from typing import Any, Dict, List, Optional, Tuple, Union

import h5py
import numpy as np
import xarray as xr
from pynxtools.dataconverter.readers.multi.reader import MultiFormatReader
from pynxtools.dataconverter.readers.utils import parse_yml

logger = logging.getLogger("pynxtools")


def recursive_parse_metadata(
    node: Union[h5py.Group, h5py.Dataset],
) -> dict:
    """Recurses through an hdf5 file, and parse it into a dictionary.

    Args:
        node (Union[h5py.Group, h5py.Dataset]): hdf5 group or dataset to parse into
            dictionary.

    Returns:
        dict: Dictionary of elements in the hdf5 path contained in node
    """
    if isinstance(node, h5py.Group):
        dictionary = {}
        for key, value in node.items():
            dictionary[key] = recursive_parse_metadata(value)

    else:
        entry = node[...]
        try:
            dictionary = entry.item()
            if isinstance(dictionary, (bytes, bytearray)):
                dictionary = dictionary.decode()
        except ValueError:
            dictionary = entry

    return dictionary


def h5_to_xarray(faddr: str, mode: str = "r") -> xr.DataArray:
    """Read xarray data from formatted hdf5 file

    Args:
        faddr (str): complete file name (including path)
        mode (str, optional): hdf5 read/write mode. Defaults to "r".

    Raises:
        ValueError: Raised if data or axes are not found in the file.

    Returns:
        xr.DataArray: output xarra data
    """
    with h5py.File(faddr, mode) as h5_file:
        # Reading data array
        try:
            data = np.asarray(h5_file["binned"]["BinnedData"])
        except KeyError as exc:
            raise ValueError(
                "Wrong Data Format, the BinnedData was not found.",
            ) from exc

        # Reading the axes
        bin_axes = []
        bin_names = []

        try:
            for axis in h5_file["axes"]:
                bin_axes.append(h5_file["axes"][axis])
                bin_names.append(h5_file["axes"][axis].attrs["name"])
        except KeyError as exc:
            raise ValueError(
                "Wrong Data Format, the axes were not found.",
            ) from exc

        # load metadata
        metadata = None
        if "metadata" in h5_file:
            metadata = recursive_parse_metadata(h5_file["metadata"])

        # Segment to change Vset to V in lens voltages
        if "file" in metadata.keys():
            for k in list(metadata["file"]):
                if "VSet" in k:
                    key = k[:-3]
                    metadata["file"][key] = metadata["file"][k]
                    del metadata["file"][k]

        coords = {}
        for name, vals in zip(bin_names, bin_axes):
            coords[name] = vals

        xarray = xr.DataArray(data, dims=bin_names, coords=coords)

        for axis in range(len(bin_axes)):
            try:
                xarray[bin_names[axis]].attrs["unit"] = h5_file["axes"][
                    f"ax{axis}"
                ].attrs["unit"]
            except (KeyError, TypeError):
                xarray[bin_names[axis]].attrs["unit"] = ""
        try:
            xarray.attrs["units"] = h5_file["binned"]["BinnedData"].attrs["units"]
            xarray.attrs["long_name"] = h5_file["binned"]["BinnedData"].attrs[
                "long_name"
            ]
        except (KeyError, TypeError):
            xarray.attrs["units"] = ""
            xarray.attrs["long_name"] = ""

        if metadata is not None:
            xarray.attrs["metadata"] = metadata

        return xarray


def iterate_dictionary(dic, key_string):
    """Recursively iterate in dictionary and give back its values"""
    keys = key_string.split("/", 1)
    if keys[0] in dic:
        if len(keys) == 1:
            return dic[keys[0]]
        if not len(keys) == 1:
            return iterate_dictionary(dic[keys[0]], keys[1])
    else:
        return None


def rgetattr(obj, attr):
    """Get attributes recursively"""

    def _getattr(obj, attr):
        return getattr(obj, attr)

    if "index" in attr:
        axis = attr.split(".")[0]
        return obj.dims.index(f"{axis}")

    return reduce(_getattr, [obj] + attr.split("."))


class MPESReader(MultiFormatReader):
    """MPES-specific reader class"""

    supported_nxdls = ["NXmpes", "NXmpes_arpes"]
    config_file: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eln_data = None

        self.extensions = {
            ".yml": self.handle_eln_file,
            ".yaml": self.handle_eln_file,
            ".json": self.set_config_file,
            ".h5": self.handle_hdf5_file,
            ".hdf5": self.handle_hdf5_file,
        }

    def handle_hdf5_file(self, file_path: str) -> Dict[str, Any]:
        """Handle hdf5 file"""
        self.data_xarray = h5_to_xarray(file_path)

        return {}

    def set_config_file(self, file_path: str) -> Dict[str, Any]:
        if self.config_file is not None:
            logger.info(f"Config file already set. Skipping the new file {file_path}.")
        self.config_file = file_path
        return {}

    def handle_eln_file(self, file_path: str) -> Dict[str, Any]:
        self.eln_data = parse_yml(
            file_path,
            parent_key="/ENTRY",
        )

        return {}

    def get_eln_data(self, key: str, path: str) -> Any:
        """Returns data from the given eln path."""
        if self.eln_data is None:
            return None

        return self.eln_data.get(path)

    def handle_objects(self, objects: Tuple[Any]) -> Dict[str, Any]:
        if isinstance(objects, xr.DataArray):
            # Should normally be a tuple, but in the
            # past a single xarray object was passed.
            # This if-clause exists for backwards compatibility
            self.data_xarray = objects
            return {}
        if (
            isinstance(objects, tuple)
            and len(objects) > 0
            and isinstance(objects[0], xr.DataArray)
        ):
            self.data_xarray = objects[0]
            return {}

        logger.info(
            f"Error while reading objects: {objects} does not contain an xarray object."
            " Skipping the objects."
        )
        return {}

    def get_data(self, key: str, path: str) -> Any:
        try:
            value = rgetattr(obj=self.data_xarray, attr=path)
            if key.split("/")[-1] == "@axes":
                return list(value)
            return value

        except ValueError:
            logger.warning(f"Incorrect axis name corresponding to the path {path}")

        except AttributeError:
            logger.warning(
                "Incorrect naming syntax or the xarray doesn't "
                f"contain entry corresponding to the path {path}"
            )

    def get_data_dims(self, key: str, path: str) -> List[str]:
        return list(map(str, self.data_xarray.dims))

    def get_attr(self, key: str, path: str) -> Any:
        return iterate_dictionary(self.data_xarray.attrs, path)


READER = MPESReader
