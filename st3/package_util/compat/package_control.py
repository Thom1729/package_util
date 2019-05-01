from .typing import List, Tuple

try:
    from package_control.package_manager import PackageManager  # type: ignore

    manager = PackageManager()

    def get_dependency_relationships() -> List[Tuple[str, str]]:
        return [
            (name, dep)
            for name in (manager.list_packages() + manager.list_dependencies())
            for dep in manager.get_dependencies(name)
        ]

except ImportError:  # pragma: nocoverage
    def get_dependency_relationships() -> List[Tuple[str, str]]:
        return []
