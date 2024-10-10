# Examples

You can find exhaustive examples how to use `pynxtools-mpes` for your ARPES research data pipeline [here](https://gitlab.mpcdf.mpg.de/nomad-lab/north/mpes/-/tree/main/example).

There are also small example files for using the `pynxtools` dataconverter with the `mpes` reader and the `NXmpes` application definition in [`tests/data/dataconverter/readers/mpes`](https://github.com/FAIRmat-NFDI/pynxtools/tree/master/tests/data/dataconverter/readers/mpes).

You can run the conversion 
```shell
dataconverter \\
    --reader mpes \\
    --nxdl NXmpes_arpes \\
    xarray_saved_small_calibration \\
    eln_data.yaml \\
    -c  config_file.json \\
    --output mpes_example.nxs
```
