import sublime_plugin
import sys

from sublime_lib import ResourcePath

from .importer import ReloadingImporter
from ..compat.package_control import get_dependency_relationships
from ..util.dependencies import get_dependents
from ..util.module_utils import module_paths

from types import ModuleType
from ..compat.typing import Container, Iterable, Tuple


def get_package_modules(
    package_names: Container[str]
) -> Iterable[Tuple[ModuleType, ResourcePath]]:
    for module in sys.modules.values():
        for file_path in module_paths(module):
            try:
                path = ResourcePath.from_file_path(file_path)
            except ValueError:
                continue
            else:
                if path.package in package_names:  # type: ignore
                    yield module, path
                    break


def reload_packages(packages: Iterable[str]) -> None:
    packages = get_dependents(packages, get_dependency_relationships())
    modules = list(get_package_modules(packages))

    sorted_modules = sorted(
        [module for module, path in modules],
        key=lambda module: module.__name__.split('.')
    )

    plugins = [
        module
        for module, path in modules
        if len(path.parts) == 3
    ]

    for module in plugins:
        sublime_plugin.unload_module(module)

    with ReloadingImporter(sorted_modules) as reload:
        for module in sorted_modules:
            try:
                reload(module)
            except FileNotFoundError as e:
                print(e)

    for module in plugins:
        sublime_plugin.load_module(module)
