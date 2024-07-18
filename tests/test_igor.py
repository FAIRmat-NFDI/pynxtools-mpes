import os
from glob import glob
from pathlib import Path

import pytest
from pynxtools.dataconverter.convert import convert


@pytest.mark.skip(reason="Skip because igor data is not in the repo yet")
def test_igor_reader(tmp_path):
    dir_path = Path(__file__).parent / "data" / "igor"
    convert(
        input_file=glob(str(dir_path / "data" / "*.ibw")),
        reader="igor_fhi",
        nxdl="NXmpes",
        output=os.path.join(dir_path / "igor_test.nxs"),
        config_file=str(dir_path / "config_file.json"),
        skip_verify=False,
        ignore_undocumented=False,
    )
