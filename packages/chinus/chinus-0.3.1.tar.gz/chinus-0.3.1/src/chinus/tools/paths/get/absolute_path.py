import os

from src.chinus.tools.paths.get.project_root import get_project_root
from pathlib import Path
from src.chinus.decorator.warning.not_used_return_value import use_return


@use_return
def get_absolute_path(project_relative_path: str, root_identifiers: set = None) -> str:
    return str(Path(os.path.join(get_project_root(root_identifiers), project_relative_path)))