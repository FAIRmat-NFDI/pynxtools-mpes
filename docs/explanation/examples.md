# Examples


# How to use it?

This is an example to use the dataconvert with the `mpes` reader and the `NXmpes` application definition.
If you want to use some example data you can find small example files in [`tests/data/dataconverter/readers/mpes`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests/data/dataconverter/readers/mpes).

```shell
dataconverter --reader mpes \\
    --nxdl NXmpes \\
    xarray_saved_small_calibration \\
    config_file.json \\
    eln_data.yaml \\
    --output mpes_example.nxs
```

The reader is a tailored parser for research data in a common format. This particular example is able to read and map hdf5 files, as well as json and yaml files. Feel free to contact FAIRmat if you want to create a parser for your research data.

# Are there detailed examples?

Yes, [here](https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-remote-tools-hub/-/tree/develop/docker/mpes) you can find exhaustive examples how to use `pynxtools` for your ARPES research data pipeline.