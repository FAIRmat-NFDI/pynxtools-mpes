# Convert MPES data and metadata to NeXus

## Who is this tutorial for?

This document is for people who want to use this reader as a standalone standardize their research data by converting these
into a NeXus standardized format.

## What should you should know before this tutorial?

- You should have a basic understanding of [FAIRmat NeXus](https://github.com/FAIRmat/nexus_definitions) and [pynxtools](https://github.com/FAIRmat/pynxtools)
- You should have a basic understanding of using Python and Jupyter notebooks via [JupyterLab](https://jupyter.org)

## What you will know at the end of this tutorial?

You will have a basic understanding how to use pynxtools-mpes for converting your MPES data to a NeXus/HDF5 file.

## Steps

### Installation
See [here](./installation.md) for how to install pynxtools together with the MPES reader plugin.

### Running the reader from the command line
An example script to run the MPES reader in `pynxtools`:
```sh
 ! dataconverter \
--reader mpes \
--nxdl NXmpes_arpes \
$<mpes-file path> \
$<eln-file path> \
-c $<config-file path> \
--output <output-file path>.nxs
```

**Congrats! You now have a FAIR NeXus file!**
