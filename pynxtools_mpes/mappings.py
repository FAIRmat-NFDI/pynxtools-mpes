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
    "Beam": "beam_TYPE[beam]",
    "unit": "@units",
    "Sample": "SAMPLE[sample]",
    "Source": "source_TYPE[source]",
    "User": "USER[user]",
    "energy_resolution": "energy_resolution/resolution",
    "momentum_resolution": "RESOLUTION[momentum_resolution]/resolution",
    "temporal_resolution": "RESOLUTION[temporal_resolution]/resolution",
    "spatial_resolution": "RESOLUTION[spatial_resolution]/resolution",
    "sample_temperature": "temperature_sensor/value",
}

REPLACE_NESTED = {
    "SAMPLE[sample]/chemical_formula": "SAMPLE[sample]/SUBSTANCE[substance]/molecular_formula_hill",
    "source_TYPE[source]/Probe": "source_TYPE[source_probe]",
    "source_TYPE[source]/Pump": "source_TYPE[source_pump]",
    "beam_TYPE[beam]/Probe": "beam_TYPE[beam_probe]",
    "beam_TYPE[beam]/Pump": "beam_TYPE[beam_pump]",
    "sample_history": "sample_history/notes",
    "ELECTRONANALYSER[electronanalyser]/RESOLUTION[momentum_resolution]": (
        "ELECTRONANALYSER[electronanalyser]/momentum_resolution"
    ),
    "ELECTRONANALYSER[electronanalyser]/RESOLUTION[spatial_resolution]": (
        "ELECTRONANALYSER[electronanalyser]/spatial_resolution"
    ),
    "SAMPLE[sample]/gas_pressure": "INSTRUMENT[instrument]/pressure_gauge/value",
    "SAMPLE[sample]/temperature": (
        "INSTRUMENT[instrument]/MANIPULATOR[manipulator]/temperature_sensor/value"
    ),
}
