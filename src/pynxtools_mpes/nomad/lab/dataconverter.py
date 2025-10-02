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

from pynxtools.nomad.dataconverter import create_eln_dict, write_yaml

m_package = Package(name="mpes_eln_exporter")


class MpesElnExporter(EntryData):
    export = Quantity(
        type=bool,
        description="Export ELN data to YAML file",
        a_eln=dict(component="BoolEditQuantity"),
        default=True,
    )
    output = Quantity(
        type=str,
        description="Output yaml file to save all the data. Default: eln_data.yaml",
        a_eln=dict(component="StringEditQuantity"),
        a_browser=dict(adaptor="RawFileAdaptor"),
        default="eln_data.yaml",
    )

    def normalize(self, archive, logger):
        super(MpesElnExporter, self).normalize(archive, logger)
        if self.export:
            self.output = (
                f"{archive.metadata.mainfile.replace('.archive.json', '')}.yaml"
            )
            eln_dict = create_eln_dict(archive)
            try:
                eln_dict["data"]["project"] = create_eln_dict(
                    archive.data.project.m_parent
                )["data"]
                eln_dict["data"]["laser"] = create_eln_dict(
                    archive.data.laser.m_parent
                )["data"]
                eln_dict["data"]["instrument"] = create_eln_dict(
                    archive.data.instrument.m_parent
                )["data"]
                eln_dict["data"]["sample"] = create_eln_dict(
                    archive.data.sample.m_parent
                )["data"]
                for index, user in enumerate(archive.data.project.users):
                    eln_dict["data"][f"user{index}"] = create_eln_dict(user.m_parent)[
                        "data"
                    ]
                del eln_dict["data"]["export"]
                del eln_dict["data"]["project"]["instrument_status"]
                del eln_dict["data"]["project"]["laser_status"]
                del eln_dict["data"]["project"]["users"]
                del eln_dict["data"]["project"]["samples"]
            except AttributeError as e:
                print(e)
                pass
            write_yaml(archive, archive.data.output, eln_dict)


m_package.__init_metainfo__()
