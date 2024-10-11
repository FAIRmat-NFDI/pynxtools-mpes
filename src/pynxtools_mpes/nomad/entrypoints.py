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
"""Entry points for mpes examples."""
try:
    from nomad.config.models.plugins import ExampleUploadEntryPoint
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

mpes_example = ExampleUploadEntryPoint(
    title="Multidimensional photoemission spectroscopy (MPES)",
    category="FAIRmat examples",
    description="""
        This example presents the capabilities of the NOMAD platform to store and standardize multidimensional photoemission spectroscopy (MPES) experimental data. It contains three major examples:

      - Taking a pre-binned file, here stored in a h5 file, and converting it into the standardized MPES NeXus format.
        There exists a [NeXus application definition for MPES](https://manual.nexusformat.org/classes/contributed_definitions/NXmpes.html#nxmpes) which details the internal structure of such a file.
      - Binning of raw data (see [here](https://www.nature.com/articles/s41597-020-00769-8) for additional resources) into a h5 file and consecutively generating a NeXus file from it.
      - An analysis example using data in the NeXus format and employing the [pyARPES](https://github.com/chstan/arpes) analysis tool to reproduce the main findings of [this paper](https://arxiv.org/pdf/2107.07158.pdf).
    """,
    path="nomad/examples",
    local_path="examples/data/uploads/mpes.zip",
)