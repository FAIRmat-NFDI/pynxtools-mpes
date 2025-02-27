import os.path
import re
from typing import Optional

import numpy as np
import yaml
import shutil

try:
    from nomad.datamodel.data import ArchiveSection, EntryData
    from nomad.metainfo import MEnum, Package, Quantity
    from nomad.units import ureg
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

from pynxtools.nomad.dataconverter import NexusDataConverter

m_package = Package(name="mpes_data_converter")


class MpesDataConverter(NexusDataConverter):
    export = Quantity(
        type=bool,
        description="Project from parent section to be exported to NeXus",
        a_eln=dict(component="BoolEditQuantity"),
        default=False,
    )

    def normalize(self, archive, logger):
        if self.export:
            self.output = f"{archive.metadata.mainfile.replace(".","_")}.nxs"
            super(MpesDataConverter, self).normalize(archive, logger)


m_package.__init_metainfo__()
