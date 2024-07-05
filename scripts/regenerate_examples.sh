#!/bin/bash
READER=mpes
NXDL=NXmpes

function update_mpes_example {
  echo "Update mpes example"
  dataconverter xarray_saved_small_calibration.h5 config_file.json --reader $READER --nxdl $NXDL --output example.nxs
}

project_dir=$(dirname $(dirname $(realpath $0)))
cd $project_dir/tests/data

update_mpes_example