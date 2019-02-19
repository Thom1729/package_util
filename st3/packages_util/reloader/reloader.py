import sublime_plugin
import sys

from sublime_lib import ResourcePath

from .dprint import dprint
from .importer import ReloadingImporter
from .resolver import resolve_dependencies

from ..util.module_utils import module_paths


def get_package_modules(package_names):
    for module in sys.modules.values():
        for file_path in module_paths(module):
            try:
                path = ResourcePath.from_file_path(file_path)
            except ValueError:
                continue
            else:
                if path.package in package_names:
                    is_plugin = len(path.parts) == 3
                    yield module, is_plugin
                    break


def reload_package(pkg_name, verbose=True):
    if pkg_name not in sys.modules:
        dprint("error:", pkg_name, "is not loaded.")
        return

    if verbose:
        dprint("begin", fill='=')

    packages = resolve_dependencies(pkg_name)
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

    with ReloadingImporter(sorted_modules, verbose) as reload:
        for module in sorted_modules:
            reload(module)

    for module in plugins:
        sublime_plugin.load_module(module)

    if verbose:
        dprint("end", fill='-')
