# How to build and run the mpes NORTH tool

The `mpes` NORTH tool provides a containerized environment for interactive MPES data analysis. See [Learn > The mpes NORTH tool](../how-tos/run-the-north-tool.md) for more information about the tool itself.

This document is for people who want to try the `mpes` NORTH tool locally, outside of a full NOMAD deployment.

## Get an image

The image is built and tested by CI (`.github/workflows/publish-north.yml`) and pushed to the registry once tests pass, tagged by what triggered the run:
- `main` for pushes to the `main` branch
- `vX.Y.Z` for version tags, and
- `pr-<number>` for a pull request (e.g. `pr-73` for the one that initialized
the NORTH tool entry point).

To get the latest published `main` build:

```bash
docker pull ghcr.io/fairmat-nfdi/pynxtools-mpes:main
```

To get a specific open PR's image instead:

```bash
docker pull --rm -p 8888:8888 ghcr.io/fairmat-nfdi/pynxtools-mpes:pr-73
```

Then continue with ["Running an image locally"](#running-an-image-locally)
below - it's the same image either way, just pulled from the registry instead
of built locally.

## Building locally

You can also build the image yourself instead of pulling one from the registry - for example, to test changes to the Dockerfile itself, or to check the build for a PR before its own CI build has finished. From the `pynxtools-mpes` package root:

```bash
docker build -f src/pynxtools_mpes/nomad/north_tools/mpes/Dockerfile \
	-t pynxtools-mpes:dev .
```

`pynxtools-mpes:dev` is just an example tag - use whatever name you like, as
long as you use the same one in the `docker run` commands below.

## Running an image locally

This applies the same way whichever image you ended up with. Run it plain, without overriding the container's default command:

```bash
docker run --rm -p 8888:8888 pynxtools-mpes:dev                      # local build
docker run --rm -p 8888:8888 ghcr.io/fairmat-nfdi/pynxtools-mpes:main # from the registry
```

It's tempting to run `docker run ... bash` instead to poke around inside the container first, but that replaces the default command rather than running alongside it - the Jupyter server never starts, so nothing ends up listening on port `8888` and the container just exits.

The container prints a URL with an access token on startup, e.g.:

```
http://127.0.0.1:8888/lab?token=<token>
```

That token is Jupyter's built-in one-time password, generated fresh each start - it stops anyone who can reach the port from getting in without it. Open the printed URL as-is (token included) in your browser.

If you ran the container detached (`docker run -d ...`) you won't see that
startup log, so fetch the token separately:

```bash
docker logs <container-name-or-id>          # look for the ".../lab?token=..." line
# or
docker exec <container-name-or-id> jupyter server list
```

For local testing only (never for a real deployment), you can disable the
token entirely:

```bash
docker run --rm -p 8888:8888 -e JUPYTER_TOKEN='' pynxtools-mpes:dev
```

## `/lab` vs. `/desktop`

The token URL lands on `/lab` (plain JupyterLab) - that's just Jupyter
Server's own default page, unrelated to NORTH. This NORTH tool's actual
xfce/VNC desktop lives at `/desktop` instead. There are two ways to get
there:

- From `/lab`, click the **Desktop** tile in the launcher.
- Or go straight there yourself: `http://127.0.0.1:8888/desktop?token=<token>`.

Testing GUI apps means testing them from inside that Desktop tab - a bare
`docker exec ... bash` has no display/VNC session running, so GUI apps won't
work from there.

When NOMAD itself opens this tool for a user (via NORTH), it routes straight
to `/desktop` automatically using the `default_url` set on the tool's
`NORTHTool` entry point - that routing only exists inside a real NOMAD
deployment, not when you run the container directly like this.
