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
try:
    from nomad.config.models.plugins import (
        ExampleUploadEntryPoint,
        AppEntryPoint,
        SchemaPackageEntryPoint,
    )
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

class MpesDataConverterEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools_mpes.nomad.lab.dataconverter import m_package

        return m_package    

class MpesElnExporterEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from pynxtools_mpes.nomad.lab.dataconverter import MpesElnExporter

        return MpesElnExporter


mpes_data_converter = MpesDataConverterEntryPoint(
    name="NeXus Dataconverter",
    description="The NeXus dataconverter to convert data into the NeXus format.",
)
