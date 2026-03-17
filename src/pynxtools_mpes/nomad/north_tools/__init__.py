from nomad.config.models.north import NORTHTool
from nomad.config.models.plugins import NORTHToolEntryPoint

mpes_north_tool = NORTHTool(
    image="ghcr.io/FAIRmat-NFDI/pynxtools-mpes/jupyter:latest",
    description="""### **Visualization and analysis tools for MPES**

    The MPES container provides multiple desktop applications for analyzing and visualizing
    multi-dimensional photoemission spectroscopy (MPES)data.""",
    short_description="Container with visualization and analysis tools for MPES.",
    external_mounts=[],
    file_extensions=["ipynb", "nxs", "h5", "hdf5"],
    # icon="", ??
    image_pull_policy="Always",
    default_url="/desktop",
    maintainer=[
        {
            "name": "Lukas Pielsticker",
            "email": "lukas.pielsticker@physik.hu-berlin.de",
        },
        {
            "name": "Laurenz Rettig",
            "email": "rettig@fhi-berlin.mpg.de",
        },
    ],
    mount_path="/home/jovyan",  # /config
    path_prefix="lab/tree",
    privileged=False,
    with_path=True,
    display_name="mpes",
)

mpes = NORTHToolEntryPoint(id_url_safe="mpes", north_tool=mpes_north_tool)
