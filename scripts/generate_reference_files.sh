#!/bin/bash
READER=mpes
NXDL=NXmpes

function update_mpes_example {
  echo "Update mpes example"
  dataconverter xarray_saved_small_calibration.h5 config_file.json --reader $READER --nxdl $NXDL --output example.nxs
}

function update_mpes_eln_example {
  echo "Update mpes example with eln file"
  dataconverter xarray_saved_small_calibration.h5 config_file.json eln_data.yaml --reader $READER --nxdl $NXDL --output example_eln.nxs
}

project_dir=$(dirname $(dirname $(realpath $0)))
cd $project_dir/tests/data

update_mpes_example
update_mpes_eln_example