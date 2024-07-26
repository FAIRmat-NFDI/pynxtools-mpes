"""
Mapping dictionaries for the MPES conversion.
"""

DEFAULT_UNITS = {
    "X": "step",
    "Y": "step",
    "t": "step",
    "tofVoltage": "V",
    "extractorVoltage": "V",
    "extractorCurrent": "A",
    "cryoTemperature": "K",
    "sampleTemperature": "K",
    "dldTimeBinSize": "ns",
    "delay": "ps",
    "timeStamp": "s",
    "energy": "eV",
    "kx": "1/A",
    "ky": "1/A",
}

CONVERT_DICT = {
    "Instrument": "INSTRUMENT[instrument]",
    "Analyzer": "ELECTRONANALYSER[electronanalyser]",
    "Manipulator": "MANIPULATOR[manipulator]",
    "Beam": "beamTYPE[beam]",
    "unit": "@units",
    "Sample": "SAMPLE[sample]",
    "Source": "sourceTYPE[source]",
    "User": "USER[user]",
    "energy_resolution": "energy_resolution/resolution",
    "momentum_resolution": "RESOLUTION[momentum_resolution]/resolution",
    "temporal_resolution": "RESOLUTION[temporal_resolution]/resolution",
    "spatial_resolution": "RESOLUTION[spatial_resolution]/resolution",
    "angular_resolution": "RESOLUTION[angular_resolution]/resolution",
    "sample_temperature": "temperature_sensor/value",
    "drain_current": "drain_current_amperemeter/value",
    "photon_energy": "energy",
}

REPLACE_NESTED = {
    "SAMPLE[sample]/chemical_formula": "SAMPLE[sample]/SUBSTANCE[substance]/molecular_formula_hill",
    "sourceTYPE[source]/Probe": "sourceTYPE[source_probe]",
    "sourceTYPE[source]/Pump": "sourceTYPE[source_pump]",
    "beamTYPE[beam]/Probe": "beamTYPE[beam_probe]",
    "beamTYPE[beam]/Pump": "beamTYPE[beam_pump]",
    "sample_history": "history/notes/description",
    "ELECTRONANALYSER[electronanalyser]/RESOLUTION[energy_resolution]": (
        "ELECTRONANALYSER[electronanalyser]/energy_resolution"
    ),
    "ELECTRONANALYSER[electronanalyser]/RESOLUTION[momentum_resolution]": (
        "ELECTRONANALYSER[electronanalyser]/momentum_resolution"
    ),
    "ELECTRONANALYSER[electronanalyser]/RESOLUTION[spatial_resolution]": (
        "ELECTRONANALYSER[electronanalyser]/spatial_resolution"
    ),
    "ELECTRONANALYSER[electronanalyser]/RESOLUTION[angular_resolution]": (
        "ELECTRONANALYSER[electronanalyser]/angular_resolution"
    ),
    "SAMPLE[sample]/gas_pressure": "INSTRUMENT[instrument]/pressure_gauge/value",
    "SAMPLE[sample]/temperature": (
        "INSTRUMENT[instrument]/MANIPULATOR[manipulator]/temperature_sensor/value"
    ),
}
