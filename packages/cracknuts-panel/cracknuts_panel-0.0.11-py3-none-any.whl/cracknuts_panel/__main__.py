import subprocess
from importlib.resources import files
import shutil
from pathlib import Path


def create_jupyter_notebook(template: str, new_ipynb_name: str):
    template = files("cracknuts_panel.template.jupyter").joinpath(f"{template}.ipynb")
    if not new_ipynb_name.endswith(".ipynb"):
        new_ipynb_name += ".ipynb"

    new_ipynb_path = Path(new_ipynb_name)
    if not new_ipynb_path.is_absolute():
        new_ipynb_path = Path.cwd().joinpath(new_ipynb_name)
    new_ipynb_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(template.as_posix(), new_ipynb_path.as_posix())
    _open_jupyter(new_ipynb_path.as_posix())


def _open_jupyter(ipynb_file: str):
    subprocess.run(["jupyter", "lab", ipynb_file])
