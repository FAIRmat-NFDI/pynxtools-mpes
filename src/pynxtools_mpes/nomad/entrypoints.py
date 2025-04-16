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
    from nomad.config.models.plugins import ExampleUploadEntryPoint, AppEntryPoint
except ImportError as exc:
    raise ImportError(
        "Could not import nomad package. Please install the package 'nomad-lab'."
    ) from exc

mpes_example = ExampleUploadEntryPoint(
    title="Multidimensional photoemission spectroscopy (MPES)",
    category="FAIRmat examples",
    description="""
        This example presents the capabilities of the NOMAD platform to store and standardize multidimensional photoemission spectroscopy (MPES) experimental data. It contains four major examples:

      - Taking a pre-binned file, here stored in a h5 file, and converting it into the standardized MPES NeXus format.
        There exists a [NeXus application definition for MPES](https://manual.nexusformat.org/classes/contributed_definitions/NXmpes.html#nxmpes) which details the internal structure of such a file.
      - Binning of raw data (see [here](https://www.nature.com/articles/s41597-020-00769-8) for additional resources) into a h5 file and consecutively generating a NeXus file from it.
      - An analysis example using data in the NeXus format and employing the [pyARPES](https://github.com/chstan/arpes) analysis tool to reproduce the main findings of [this paper](https://arxiv.org/pdf/2107.07158.pdf).
      - Importing angle-resolved data stored in NXmpes_arpes, and convert these into momentum space coordinates using tools in pyARPES.
    """,
    plugin_package="pynxtools_mpes",
    resources=["nomad/examples/*"],
)

from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemHistogram,
    MenuItemPeriodicTable,
    MenuItemTerms,
    MenuSizeEnum,
    SearchQuantities,
    AxisLimitedScale,
    Markers,
    Axis,
)

schema = "pynxtools.nomad.schema.Root"

mpes_app = AppEntryPoint(
    name="MpesApp",
    description="Simple NXmpes NeXus app.",
    app=App(
        # Label of the App
        label="MPES",
        # Path used in the URL, must be unique
        path="mpesapp",
        # Used to categorize apps in the explore menu
        category="Experiment",
        # Brief description used in the app menu
        description="A simple search app customized for NXmpes NeXus data.",
        # Longer description that can also use markdown
        readme="This is a simple App to support basic search for NXmpes NeXus based Experiment Entries.",
        # If you want to use quantities from a custom schema, you need to load
        # the search quantities from it first here. Note that you can use a glob
        # syntax to load the entire package, or just a single schema from a
        # package.
        search_quantities=SearchQuantities(
            include=[f"*#{schema}"],
        ),
        # Controls which columns are shown in the results table
        columns=[
            Column(title="Entry ID", search_quantity="entry_id", selected=True),
            Column(
                title="File Name",
                search_quantity=f"mainfile",
                selected=True,
            ),
            Column(
                title="Start Time",
                search_quantity=f"data.ENTRY[*].start_time#{schema}",
                selected=True,
            ),
            Column(
                title="Description",
                search_quantity=f"data.ENTRY[*].experiment_description__field#{schema}",
                selected=True,
            ),
            Column(
                title="Author",
                search_quantity=f"data.ENTRY[*].USER[*].name__field#{schema}",
                selected=True,
            ),
            Column(
                title="Sample",
                search_quantity=f"data.ENTRY[*].SAMPLE[*].name__field#{schema}",
                selected=True,
            ),
            Column(
                title="Sample ID",
                search_quantity=f"data.ENTRY[*].SAMPLE[*].identifierNAME__field#{schema}",
                selected=False,
            ),
            Column(
                title="Definition",
                search_quantity=f"data.ENTRY[*].definition__field#{schema}",
                selected=True,
            ),
        ],
        # Dictionary of search filters that are always enabled for queries made
        # within this app. This is especially important to narrow down the
        # results to the wanted subset. Any available search filter can be
        # targeted here. This example makes sure that only entries that use
        # MySchema are included.
        filters_locked={
            f"data.ENTRY.definition__field#{schema}": [
                "NXmpes",
                "NXmpes_arpes",
                "NXxps",
            ],
        },
        # Controls the menu shown on the left
        menu=Menu(
            size=MenuSizeEnum.MD,
            title="Menu",
            items=[
                Menu(
                    title="Material",
                    size=MenuSizeEnum.XXL,
                    items=[
                        MenuItemPeriodicTable(
                            quantity="results.material.elements",
                        ),
                        MenuItemTerms(
                            title="Chemical Formula",
                            quantity="results.material.chemical_formula_iupac",
                            width=6,
                            options=10,
                        ),
                        MenuItemTerms(
                            title="Sample Name",
                            quantity=f"data.ENTRY.SAMPLE.name__field#{schema}",
                            width=6,
                            options=10,
                        ),
                        MenuItemHistogram(
                            x="results.material.n_elements",
                        ),
                    ],
                ),
                Menu(
                    title="Authors / Origin",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Entry Author",
                            search_quantity=f"data.ENTRY.USER.name__field#{schema}",
                            width=12,
                            options=5,
                        ),
                        MenuItemTerms(
                            title="Upload Author",
                            search_quantity=f"authors.name",
                            width=12,
                            options=5,
                        ),
                        MenuItemTerms(
                            title="Affiliation",
                            search_quantity=f"data.ENTRY.USER.affiliation__field#{schema}",
                            width=12,
                            options=5,
                        ),
                    ],
                ),
                Menu(
                    title="Instrument",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Instrument Name",
                            quantity=f"data.ENTRY.INSTRUMENT.name__field#{schema}",
                            width=12,
                            options=10,
                        ),
                        MenuItemHistogram(
                            title="Energy Resolution",
                            x=Axis(
                                title="Energy Resolution",
                                search_quantity=f"data.ENTRY.INSTRUMENT.energy_resolution.resolution__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Angular Resolution",
                            x=Axis(
                                title="Angular Resolution",
                                search_quantity=f"data.ENTRY.INSTRUMENT.angular_resolution.resolution__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Momentum Resolution",
                            x=Axis(
                                title="Momentum Resolution",
                                search_quantity=f"data.ENTRY.INSTRUMENT.momentum_resolution.resolution__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Spatial Resolution",
                            x=Axis(
                                title="Spatial Resolution",
                                search_quantity=f"data.ENTRY.INSTRUMENT.spatial_resolution.resolution__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Temporal Resolution",
                            x=Axis(
                                title="Temporal Resolution",
                                search_quantity=f"data.ENTRY.INSTRUMENT.temporal_resolution.resolution__field#{schema}#float",
                            ),
                        ),
                    ],
                ),
                Menu(
                    title="Sample Environment",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Situation",
                            quantity=f"data.ENTRY.SAMPLE.situation__field#{schema}",
                            width=12,
                            options=3,
                        ),
                        MenuItemHistogram(
                            title="Sample temperature",
                            x=Axis(
                                title="Sample Temperature",
                                search_quantity=f"data.ENTRY.SAMPLE.temperature_env.temperature_sensor.value__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Sample drain current",
                            x=Axis(
                                title="Sample drain current",
                                search_quantity=f"data.ENTRY.SAMPLE.drain_current_env.ammeter.value__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Residual gas pressure",
                            x=Axis(
                                title="Residual gas pressure",
                                search_quantity=f"data.ENTRY.SAMPLE.gas_pressure_env.pressure_gauge.value__field#{schema}#float",
                            ),
                        ),
                    ],
                ),
                Menu(
                    title="Probe Beam",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Probe Source",
                            quantity=f"data.ENTRY.INSTRUMENT.source_probe.name__field#{schema}#str",
                            width=12,
                            options=5,
                        ),
                        MenuItemHistogram(
                            title="Probe beam energy",
                            x=Axis(
                                title="Probe beam energy",
                                search_quantity=f"data.ENTRY.INSTRUMENT.beam_probe.incident_energy__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Probe beam polarization",
                            x=Axis(
                                title="Probe beam polarization",
                                search_quantity=f"data.ENTRY.INSTRUMENT.beam_probe.incident_polarization__field#{schema}#float",
                            ),
                        ),
                    ],
                ),
                Menu(
                    title="Pump Beam",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Pump Source",
                            quantity=f"data.ENTRY.INSTRUMENT.source_pump.name__field#{schema}#str",
                            width=12,
                            options=5,
                        ),
                        MenuItemHistogram(
                            title="Pump beam energy",
                            x=Axis(
                                title="Pump beam energy",
                                search_quantity=f"data.ENTRY.INSTRUMENT.beam_pump.incident_energy__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Pump beam polarization",
                            x=Axis(
                                title="Pump beam polarization",
                                search_quantity=f"data.ENTRY.INSTRUMENT.beam_pump.incident_polarization__field#{schema}#float",
                            ),
                        ),
                        MenuItemHistogram(
                            title="Pump beam fluence",
                            x=Axis(
                                title="Pump beam fluence",
                                search_quantity=f"data.ENTRY.INSTRUMENT.beam_pump.fluence__field#{schema}#float",
                            ),
                        ),
                    ],
                ),
                Menu(
                    title="Data Range",
                    size=MenuSizeEnum.LG,
                    items=[
                        MenuItemTerms(
                            title="Scan Axes",
                            quantity=f"data.ENTRY.DATA.___axes#{schema}#str",
                            width=12,
                            options=10,
                        ),
                        MenuItemHistogram(
                            title="Min. energy",
                            x=Axis(
                                title="Min. energy",
                                search_quantity=f"data.ENTRY.DATA.energy__min#{schema}#float",
                            ),
                            width=6,
                        ),
                        MenuItemHistogram(
                            title="Max. energy",
                            x=Axis(
                                title="Max. energy",
                                search_quantity=f"data.ENTRY.DATA.energy__max#{schema}#float",
                            ),
                            width=6,
                        ),
                        MenuItemHistogram(
                            title="Min. kx",
                            x=Axis(
                                title="Min. kx",
                                search_quantity=f"data.ENTRY.DATA.kx__min#{schema}#float",
                            ),
                            width=6,
                        ),
                        MenuItemHistogram(
                            title="Max. kx",
                            x=Axis(
                                title="Max. kx",
                                search_quantity=f"data.ENTRY.DATA.kx__max#{schema}#float",
                            ),
                            width=6,
                        ),
                        MenuItemHistogram(
                            title="Min. ky",
                            x=Axis(
                                title="Min. ky",
                                search_quantity=f"data.ENTRY.DATA.ky__min#{schema}#float",
                            ),
                            width=6,
                        ),
                        MenuItemHistogram(
                            title="Max. ky",
                            x=Axis(
                                title="Max. ky",
                                search_quantity=f"data.ENTRY.DATA.ky__max#{schema}#float",
                            ),
                            width=6,
                        ),
                        MenuItemHistogram(
                            title="Min. delay",
                            x=Axis(
                                title="Min. delay",
                                search_quantity=f"data.ENTRY.DATA.delay__min#{schema}#float",
                            ),
                            width=6,
                        ),
                        MenuItemHistogram(
                            title="Max. delay",
                            x=Axis(
                                title="Max. delay",
                                search_quantity=f"data.ENTRY.DATA.delay__max#{schema}#float",
                            ),
                            width=6,
                        ),
                    ],
                ),
                MenuItemHistogram(
                    title="Start Time",
                    x=f"data.ENTRY.start_time__field#{schema}",
                    autorange=True,
                ),
                MenuItemHistogram(
                    title="Upload Creation Time",
                    x=f"upload_create_time",
                    autorange=True,
                ),
            ],
        ),
        # Controls the default dashboard shown in the search interface
        dashboard={
            "widgets": [
                {
                    "type": "terms",
                    "show_input": False,
                    "scale": "linear",
                    "quantity": "results.material.chemical_formula_iupac",
                    "title": "Material",
                    "layout": {
                        "sm": {"minH": 3, "minW": 3, "h": 5, "w": 4, "y": 0, "x": 0},
                        "md": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 0},
                        "lg": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 0},
                        "xl": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 0},
                        "xxl": {"minH": 3, "minW": 3, "h": 8, "w": 7, "y": 0, "x": 0},
                    },
                },
                {
                    "type": "histogram",
                    "show_input": False,
                    "autorange": True,
                    "nbins": 30,
                    "scale": "linear",
                    "x": Axis(
                        title="Sample Temperature",
                        search_quantity=f"data.ENTRY.SAMPLE.temperature_env.temperature_sensor.value__field#{schema}#float",
                    ),
                    "title": "Sample Temperature",
                    "layout": {
                        "sm": {"minH": 3, "minW": 3, "h": 5, "w": 4, "y": 0, "x": 4},
                        "md": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 6},
                        "lg": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 6},
                        "xl": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 6},
                        "xxl": {"minH": 3, "minW": 3, "h": 8, "w": 7, "y": 0, "x": 7},
                    },
                },
                # {
                #     "type": "terms",
                #     "show_input": False,
                #     "scale": "linear",
                #     "quantity": f"data.ENTRY.data.___axes#{schema}#str",
                #     "title": "Dataset Axes",
                #     "layout": {
                #         "sm": {"minH": 3, "minW": 3, "h": 5, "w": 4, "y": 0, "x": 8},
                #         "md": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 12},
                #         "lg": {"minH": 3, "minW": 3, "h": 5, "w": 5, "y": 0, "x": 10},
                #         "xl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 8},
                #         "xxl": {"minH": 3, "minW": 3, "h": 7, "w": 4, "y": 0, "x": 8},
                #     },
                # },
                {
                    "type": "scatter_plot",
                    "x": AxisLimitedScale(
                        title="# Data Points",
                        search_quantity=f"data.ENTRY[*].DATA[*].data__size#{schema}#int",
                        scale="log",
                    ),
                    "y": AxisLimitedScale(
                        title="Acquisition time (s)",
                        search_quantity=f"data.ENTRY[*].collection_time__field#{schema}#int",
                        scale="log",
                    ),
                    "markers": Markers(
                        color=Axis(
                            title="Data Axes",
                            search_quantity=f"data.ENTRY[*].DATA[*].___axes#{schema}#str",
                        )
                    ),
                    "title": "Scan Quality",
                    "layout": {
                        "sm": {"minH": 3, "minW": 3, "h": 5, "w": 4, "y": 0, "x": 8},
                        "md": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 12},
                        "lg": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 12},
                        "xl": {"minH": 3, "minW": 3, "h": 7, "w": 6, "y": 0, "x": 12},
                        "xxl": {"minH": 3, "minW": 3, "h": 8, "w": 7, "y": 0, "x": 14},
                    },
                },
            ]
        },
    ),
)
