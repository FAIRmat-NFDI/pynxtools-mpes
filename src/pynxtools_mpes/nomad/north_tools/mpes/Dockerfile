ARG UV_VERSION=0.9
ARG PLUGIN_NAME=pynxtools-mpes
ARG BASE_IMAGE=ghcr.io/fairmat-nfdi/nomad-north-desktop-base
ARG IMAGE_TAG=main

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_stage

# Standalone H5Web app (see config/h5web-view): reads HDF5/NeXus files
# client-side via WebAssembly, no backend needed. Built once here so the final
# image only carries the static output, not a Node toolchain.
FROM node:22-slim AS h5web_build_stage
WORKDIR /build
COPY src/pynxtools_mpes/nomad/north_tools/mpes/h5web-standalone .
RUN npm install && npm run build

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
        # needed by E2's own notebook cell to extract the downloaded WSe2.zip
        unzip \
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

# ---- Chrome ----
# --no-sandbox: this container's user namespace can't set up Chromium's setuid
# sandbox, so Chrome fails to start without it; --disable-dev-shm-usage avoids
# the small default /dev/shm size causing renderer crashes; --password-store=basic
# stops Chrome from prompting to create a system keyring, since none runs in
# this minimal xfce container; --disable-gpu-sandbox/--use-gl=angle/
# --use-angle=swiftshader/--enable-unsafe-swiftshader make WebGL (used by
# H5Web's plotting) fall back to software rendering instead of failing outright
# with no real GPU in the container.
#
# Patched into google-chrome-stable's own wrapper script (the last line of
# /opt/google/chrome/google-chrome, which /usr/bin/google-chrome-stable
# symlinks to), not just its .desktop file's Exec line - google-chrome-stable
# also registers itself as the system's x-www-browser alternative, which is
# what xfce's panel "web browser" launcher and exo's WebBrowser helper resolve
# to; patching only the .desktop file leaves those other paths launching
# Chrome unflagged.
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
 && dpkg -i google-chrome-stable_current_amd64.deb \
 && rm google-chrome-stable_current_amd64.deb \
 && sed -i 's|exec -a "\$0" "\$HERE/chrome" "\$@"|exec -a "$0" "$HERE/chrome" --no-sandbox --disable-dev-shm-usage --password-store=basic --disable-gpu-sandbox --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader "$@"|' \
        /opt/google/chrome/google-chrome

# h5web-view: serves the standalone H5Web app (built above) locally and opens
# it in Chrome, so a file can be explored/plotted with real H5Web, not just a
# structure browser. Icon is H5Web's own favicon; there's no icon-theme name
# for it, so it's placed by hand like silx's icon below.
COPY --from=h5web_build_stage /build/dist /opt/h5web-standalone
COPY "src/pynxtools_mpes/nomad/north_tools/mpes/config/h5web-view" /usr/local/bin/h5web-view
RUN chmod 755 /usr/local/bin/h5web-view \
 && mkdir -p /usr/share/icons/hicolor/192x192/apps \
 && wget -q -O /usr/share/icons/hicolor/192x192/apps/h5web.png \
        https://raw.githubusercontent.com/silx-kit/h5web/main/apps/demo/public/favicon192.png \
    # earlier package installs already generated hicolor's icon-theme.cache;
    # GTK/xfce prefer that cache over scanning the directory, so it has to be
    # regenerated or the new icon is silently ignored.
 && gtk-update-icon-cache -f /usr/share/icons/hicolor/

# ---- GUI env variables not defined in desktop-base ----
ENV DISPLAY=:1.0
ENV XDG_RUNTIME_DIR=/tmp/runtime-jovyan/
ENV LIBGL_ALWAYS_SOFTWARE=1
# TurboVNC's Xvnc has incomplete X MIT-SHM support, which crashes Qt
# applications (silx, nexpy, punx, ...) that default to using it for pixmaps.
ENV QT_X11_NO_MITSHM=1

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

# ---- VS Code (native desktop app, not code-server) ----
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg \
 && sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list' \
 && apt-get update -y \
 && apt-get install -y code \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

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

# Copied to /opt, not ${HOME}, so the full source checkout (tests/, docs/, CI
# config, etc. - not just the example notebooks users actually want) doesn't
# clutter the home directory users see in JupyterLab/VS Code/the file manager.
COPY --chown=${NB_USER}:${NB_GID} . /opt/${PLUGIN_NAME}

WORKDIR /opt/${PLUGIN_NAME}

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
    # Use inexact to avoid removing pre-installed packages in the environment.
    # --no-editable installs pynxtools-mpes as a regular site-packages copy, not
    # a link back to this checkout, so the image doesn't depend on the source
    # tree surviving in its current form.
    uv sync --group north --inexact --no-editable

WORKDIR ${HOME}
# /opt/${PLUGIN_NAME} is kept (not removed) because the example notebooks the
# CI test step runs live under its src/ tree - the package install itself no
# longer depends on it (--no-editable above). It stays out of ${HOME}, so users
# browsing the home directory don't see the whole source checkout.

# Menu entry and desktop icon for the silx viewer (HDF5/EDF/SPEC). silx ships
# its own icon in its installed package data but doesn't register it with the
# icon theme, so the launcher entry can't find it by name unless it's copied
# there.
RUN mkdir -p "${HOME}/.local/share/applications" "${HOME}/.local/share/icons/hicolor/32x32/apps" "${HOME}/Desktop" \
 && cp "$(python3 -c 'import os, silx; print(os.path.dirname(silx.__file__))')/resources/gui/icons/silx.png" \
       "${HOME}/.local/share/icons/hicolor/32x32/apps/silx.png"
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/silx-view.desktop" "${HOME}/.local/share/applications/silx-view.desktop"
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/silx-view.desktop" "${HOME}/Desktop/silx-view.desktop"
RUN chmod 755 "${HOME}/Desktop/silx-view.desktop"

# Desktop icon for Chrome, reusing its own (already-patched, see above)
# desktop entry instead of maintaining a second copy of it.
RUN cp /usr/share/applications/google-chrome.desktop "${HOME}/Desktop/google-chrome.desktop" \
 && chown ${NB_UID}:${NB_GID} "${HOME}/Desktop/google-chrome.desktop" \
 && chmod 755 "${HOME}/Desktop/google-chrome.desktop"

# Menu entry and desktop icon for h5web-view (see its own install above).
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/h5web-view.desktop" "${HOME}/.local/share/applications/h5web-view.desktop"
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/h5web-view.desktop" "${HOME}/Desktop/h5web-view.desktop"
RUN chmod 755 "${HOME}/Desktop/h5web-view.desktop"

# TurboVNC keyboard-layout workaround: without -noserverkeymap, the desktop
# ignores the client's actual host keyboard layout (e.g. German umlauts
# render as neighboring QWERTY keys). See config/turbovncserver.conf.
# TODO: remove once nomad-north-desktop-base carries this fix upstream, since
# every desktop-based NORTH tool inherits the same TurboVNC install.
RUN mkdir -p "${HOME}/.vnc"
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/turbovncserver.conf" "${HOME}/.vnc/turbovncserver.conf"

# VS Code: extensions, desktop icon, and pre-trusting that icon so xfce doesn't prompt
# "untrusted launcher" on first double-click.
# DONT_PROMPT_WSL_INSTALL suppresses the `code` CLI's interactive "install inside WSL
# anyway?" prompt, which it emits whenever the build host's kernel identifies as WSL (e.g.
# Docker Desktop on WSL2) — a no-op on a real Linux build host, where no prompt appears.
ENV DONT_PROMPT_WSL_INSTALL=1
RUN /usr/bin/code --install-extension eamodio.gitlens \
 && /usr/bin/code --install-extension h5web.vscode-h5web \
 && /usr/bin/code --install-extension ms-toolsai.jupyter \
 && /usr/bin/code --install-extension redhat.vscode-yaml \
 && /usr/bin/code --install-extension ms-python.python \
 && /usr/bin/code --install-extension ms-python.isort \
 && /usr/bin/code --install-extension redhat.vscode-xml

RUN mkdir -p "${HOME}/Desktop" "${HOME}/.config/autostart"
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/code.desktop" "${HOME}/Desktop/code.desktop"
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/autostart.desktop" "${HOME}/.config/autostart/autostart.desktop"
COPY --chown=${NB_UID}:${NB_GID} "src/pynxtools_mpes/nomad/north_tools/mpes/config/autostart_code" "${HOME}/.config/autostart/autostart"
RUN chmod 755 "${HOME}/Desktop/code.desktop" \
    "${HOME}/.config/autostart/autostart.desktop" \
    "${HOME}/.config/autostart/autostart"

# allow lsp server to access files outside home
RUN ln -s / .lsp_symlink \
 && jupyter lab server --generate-config \
 && echo "c.ContentsManager.allow_hidden=True" >> ${HOME}/.jupyter/jupyter_lab_config.py

EXPOSE 8888
