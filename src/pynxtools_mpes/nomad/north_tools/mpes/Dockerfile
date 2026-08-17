ARG UV_VERSION=0.9
ARG PLUGIN_NAME=pynxtools-mpes
ARG BASE_IMAGE=ghcr.io/fairmat-nfdi/nomad-north-desktop-base
ARG IMAGE_TAG=main

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_stage

FROM ${BASE_IMAGE}:${IMAGE_TAG}

ARG PLUGIN_NAME

COPY --from=uv_stage /uv /uvx /bin/

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# ---- Packages that were in original desktop stage but NOT in desktop-base ----
RUN apt-get -y -qq update \
 && apt-get -y -qq install \
        vim \
        xdg-utils \
        # needed by uv to fetch the git-sourced arpes dependency in the north group
        git \
        # needed to build north-group deps that ship no cp313 wheel
        build-essential \
    # chown $HOME to workaround that the xorg installation creates a
    # /home/jovyan/.cache directory owned by root
    # Create /opt/install to ensure it's writable by pip        
 && mkdir -p /opt/install \
 && chown -R $NB_UID:$NB_GID /opt/install \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# TigerVNC block was in original (TODO: we should decide as TurboVNC ≠ TigerVNC)
RUN apt-get -y -qq update \
 && apt-get -y -qq install \
        tigervnc-standalone-server \
        tigervnc-xorg-extension \
        websockify \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- Chrome ----
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
 && dpkg -i google-chrome-stable_current_amd64.deb \
 && rm google-chrome-stable_current_amd64.deb

# ---- GUI env variables not defined in desktop-base ----
ENV DISPLAY=:1.0
ENV XDG_RUNTIME_DIR=/tmp/runtime-jovyan/
ENV LIBGL_ALWAYS_SOFTWARE=1

RUN apt-get -y -qq update \
 && apt-get -y -qq install --no-install-recommends \
      curl \
      # Requirements for the QT application
      libxcb-icccm4 \
      libxcb-image0 \
      libxcb-keysyms1 \
      libxcb-render-util0 \
      libxcb-xinerama0 \
      libxcb-xkb1 \
      libxkbcommon-x11-0 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*


# Set timezone to Europe/Berlin
# ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}
WORKDIR "${HOME}"

# uv env
ENV UV_PROJECT_ENVIRONMENT=${CONDA_DIR} \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    # Use python from conda which is default for base-notebook
    # so that uv pip and pip refer to the same python
    # If needed one can create another venv with 'uv venv'
    UV_SYSTEM_PYTHON=1

COPY --chown=${NB_USER}:${NB_GID} . ${HOME}/${PLUGIN_NAME}

WORKDIR ${HOME}/${PLUGIN_NAME}

# https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
# Install dependencies
# The build context is a git submodule checkout. Its .git file points to the
# superproject's Git metadata, so setuptools-scm cannot determine the package
# version from Git.
#
# The package-specific variable name (not the generic
# SETUPTOOLS_SCM_PRETEND_VERSION) is required because other north-group dependencies built in the
# same sync also use setuptools-scm; the generic variable would force the same fallback version
# onto them too, which breaks their own version resolution. Derive a fallback version from
# the CITATION.cff file.
#
# The result must clear the minimum version required by sed-processor.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    export SETUPTOOLS_SCM_PRETEND_VERSION_FOR_PYNXTOOLS_MPES=$(grep '^version:' CITATION.cff | cut -d' ' -f2) && \
    # Use inexact to avoid removing pre-installed packages in the environment
    # We do not use ``--no-install-project`` here, as we want to install pynxtools-mpes
    uv sync --group north --inexact

WORKDIR ${HOME}
# Note: pynxtools-mpes is installed editable (not `--no-install-project`), so its site-packages
# entry points back at this checkout — do not remove ${HOME}/${PLUGIN_NAME} here, that would
# break the import.

# Desktop menu entry for the silx viewer (HDF5/EDF/SPEC)
RUN mkdir -p "${HOME}/.local/share/applications"
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/silx-view.desktop" "${HOME}/.local/share/applications/silx-view.desktop"

# allow lsp server to access files outside home
RUN ln -s / .lsp_symlink \
 && jupyter lab server --generate-config \
 && echo "c.ContentsManager.allow_hidden=True" >> ${HOME}/.jupyter/jupyter_lab_config.py

EXPOSE 8888
