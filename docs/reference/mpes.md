# Data from MPES instruments

The reader supports [HDF5](https://www.hdfgroup.org/solutions/hdf5/) created using the MPES instruments at the [Fritz Haber Institute of the Max Planck Soeciety (FHI)](https://www.fhi.mpg.de/de).

The reader for the SPECS data can be found [here](https://github.com/FAIRmat-NFDI/pynxtools-mpes/blob/main/pynxtools_mpes/reader.py).

## .sle data

<!-- How is this data structured --> 

Example data for the SLE reader is available [here](https://github.com/FAIRmat-NFDI/pynxtools-mpes/tree/main/tests/data).

The example conversion can be run with the following command.
```console
user@box:~$ dataconverter xarray_saved_small_calibration.h5 eln_data.yaml -c config_file.json --reader mpes --nxdl NXmpes_arpes --output example_eln.nxs
```

