import os

from chinu9653s.src.decorator.warning.not_used_return_value import use_return
from chinu9653s.src.tools.paths.get.project_root import get_project_root
from pathlib import Path


@use_return
def get_absolute_path(project_relative_path: str, root_identifiers: set = None) -> str:
    return str(Path(os.path.join(get_project_root(root_identifiers), project_relative_path)))