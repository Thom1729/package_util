from ..compat.typing import List, Iterable, Set, Tuple

DependencyRelationships = List[Tuple[str, str]]

try:
    from package_control.package_manager import PackageManager  # type: ignore

    manager = PackageManager()

    def get_dependency_relationships() -> DependencyRelationships:
        return [
            (name, dep)
            for name in (manager.list_packages() + manager.list_dependencies())
            for dep in manager.get_dependencies(name)
        ]

except ImportError:  # pragma: nocoverage
    def get_dependency_relationships() -> DependencyRelationships:
        return []


def get_dependents(
    initial: Iterable[str],
    dependency_relationships: DependencyRelationships
) -> Set[str]:
    recursive_dependencies = set()  # type: Set[str]

    def rec(name: str) -> None:
        if name in recursive_dependencies:
            return

        recursive_dependencies.add(name)

        for l, r in dependency_relationships:
            if r == name:
                rec(l)

    for d in initial:
        rec(d)

    return recursive_dependencies
