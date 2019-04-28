import sublime_plugin
import sys

from sublime_lib import ResourcePath

from .importer import ReloadingImporter
from .resolver import get_dependency_relationships, get_dependents

from ..util.module_utils import module_paths
from types import ModuleType
from ..compat.typing import Container, Iterable, Tuple


def get_package_modules(
    package_names: Container[str]
) -> Iterable[Tuple[ModuleType, bool]]:
    for module in sys.modules.values():
        for file_path in module_paths(module):
            try:
                path = ResourcePath.from_file_path(file_path)
            except ValueError:
                continue
            else:
                if path.package in package_names:  # type: ignore
                    is_plugin = len(path.parts) == 3
                    yield module, is_plugin
                    break


def reload_package(pkg_name: str) -> None:
    packages = get_dependents({pkg_name}, get_dependency_relationships())
    modules = list(get_package_modules(packages))

    sorted_modules = sorted(
        [module for module, is_plugin in modules],
        key=lambda module: module.__name__.split('.')
    )

    plugins = [
        module
        for module, is_plugin in modules
        if is_plugin
    ]

    for module in plugins:
        sublime_plugin.unload_module(module)

    with ReloadingImporter(sorted_modules) as reload:
        for module in sorted_modules:
            reload(module)

    for module in plugins:
        sublime_plugin.load_module(module)
