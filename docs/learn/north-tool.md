# The mpes NORTH tool

This document is for people who want to try the `mpes` NORTH tool locally, outside of a full NOMAD deployment.

The mpes NORTH tool provides a containerized environment for interactive analysis with the `pynxtools-mpes` plugin and related ARPES data analysis software. It has two sides, both reachable from the same running container:
- a JupyterLab environment for notebook-driven data processing and conversion, and
- an `xfce` desktop for GUI tools that are not notebook-based.

See [How-To > Build and run the mpes NORTH tool](../how-tos/run-the-north-tool.md) for guide on building and running the NORTH tool.

## What's installed

Notebook/library side (the `north` dependency group in `pyproject.toml`):

- `pynxtools`/`pynxtools-mpes` - convert raw MPES data to NeXus (`pynxtools` dataconverter)
- `sed-processor` - a time-resolved ARPES postprocessing pipeline (distortion correction, momentum/energy/delay calibration, binning) for raw event-based detector data
- `specsanalyzer` - processing for SPECS hemispherical analyzer data
- `arpes` (pyARPES, FAIRmat-NFDI fork) - loading, k-space conversion, and analysis of ARPES data, including its Qt-based `qt_tool` viewer
- `jupyterlab_h5web` - interactive HDF5/NeXus visualization inline in JupyterLab (also available as a VS Code extension)
- `h5glance` - lightweight HDF5/NeXus structure browser (terminal or static HTML)
- `punx` - NeXus file validation and visualization
- `nexpy`, `silx` - Qt-based standalone NeXus/HDF5 viewers (see below)

On the Desktop side, there are multiple options as well (apps with a menu entry and/or Desktop icon):

- **silx view** - browse HDF5/EDF/SPEC files
- **h5glance view** - pick a file and browse its structure as static HTML in Chrome (no interactive H5Web-style plotting; that lives in JupyterLab/VS Code instead)
- **Google Chrome** - view rendered outputs, documentation, or the h5glance-view output (beside its typical browser features)
- **VS Code** - edit notebooks/scripts/config, with the Python, Jupyter, YAML, XML, GitLens, and H5Web extensions preinstalled
- **nexpy** - launch from a terminal (no desktop icon yet)

## Typical ways of working

- **Convert and inspect a measurement file**: open `E1 Convert to NeXus.ipynb` (or one of the other example notebooks under `src/pynxtools_mpes/nomad/example_uploads/example/`) in `/lab`, run the conversion, then view the result inline with `jupyterlab_h5web` or via the silx/H5Web desktop apps.
- **Full trARPES postprocessing**: work through `sed-processor`'s pipeline in a notebook (see `E2 ARPES postprocessing.ipynb`) - distortion correction, calibration, binning - ending in a NeXus file.
- **k-space conversion and further analysis**: use `arpes` in a notebook (`E4 Convert to k-space.ipynb`) to load a NeXus file and convert/analyze it in momentum space; `qt_tool`-style interactive plots render into the Desktop tab, not inline in the notebook (see [How-To > Build and run the mpes NORTH tool](../how-tos/run-the-north-tool.md)).
- **Quick structure/validity checks without writing code**: `punx tree`/`punx validate` from a terminal, or the silx-view/H5Web desktop apps for a GUI look.
