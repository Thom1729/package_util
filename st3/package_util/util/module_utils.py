from types import ModuleType
from ..compat.typing import List, Iterable


def public_members(module: ModuleType) -> List[str]:
    try:
        return module.__all__  # type: ignore
    except AttributeError:
        return [name for name in dir(module) if not name.startswith('_')]


def module_paths(module: ModuleType) -> Iterable[str]:
    try:
        yield module.__file__
    except AttributeError:
        pass

    try:
        yield from module.__path__  # type: ignore
    except AttributeError:
        pass
