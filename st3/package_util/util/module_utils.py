from types import ModuleType
from ..compat.typing import List, Generator


def public_members(module: ModuleType) -> List[str]:
    try:
        return module.__all__  # type: ignore
    except AttributeError:
        return [name for name in dir(module) if not name.startswith('_')]


def module_paths(module: ModuleType) -> Generator[str, None, None]:
    try:
        yield module.__file__
    except AttributeError:
        pass

    try:
        yield from module.__path__  # type: ignore
    except AttributeError:
        pass
