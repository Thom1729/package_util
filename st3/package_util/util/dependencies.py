from ..compat.typing import List, Iterable, Set, Tuple


def get_dependents(
    initial: Iterable[str],
    dependency_relationships: List[Tuple[str, str]]
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
