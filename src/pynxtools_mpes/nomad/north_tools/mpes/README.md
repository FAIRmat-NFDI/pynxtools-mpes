# pynxtools-mpes - NORTH Jupyter tool

This directory contains the NORTH tool configuration and Dockerfile for programmatic creation of a Jupyter-based NOMAD NORTH tool.

## Quick start

The mpes NORTH tool provides a containerized environment for interactive analysis with the pynxtools-mpes plugin.

## Building and testing

Build the Docker image locally from package root:

```bash
docker build -f src/pynxtools_mpes/north_tools/mpes/Dockerfile \
	-t ghcr.io/FAIRmat-NFDI/pynxtools-mpes:latest .
```

Test the image:

```bash
docker run -p 8888:8888 ghcr.io/FAIRmat-NFDI/pynxtools-mpes:latest
```

Access JupyterLab at `http://localhost:8888`.

## Documentation

For comprehensive guidance, you can find information about the `NORTHTool` and `NorthToolEntryPoint` classes in
the [main NOMAD documentation](https://nomad-lab.eu/prod/v1/docs/). These resources cover entry point configuration, image structure, and dependency management.

- [How-to > ... > How to create a NORTH tool](https://fairmat-nfdi.github.io/nomad-docs/howto/plugins/types/north_tools.html)
- [Reference > ... > NorthToolEntryPoint](https://fairmat-nfdi.github.io/nomad-docs/reference/plugins.html#northtoolentrypoint)
- [Reference > ... > NORTHTool](https://fairmat-nfdi.github.io/nomad-docs/reference/config.html#northtool)
