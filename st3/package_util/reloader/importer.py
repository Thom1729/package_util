import builtins
import imp
from inspect import ismodule
from contextlib import contextmanager

from ..util.module_utils import public_members

from types import ModuleType, TracebackType
from ..compat.typing import Callable, Dict, Generator, Iterable, Optional, Tuple


Scope = Optional[Dict[str, object]]


class ReloadingImporter():
    _orig___import__ = None  # type: Callable[[str, Scope, Scope, Tuple, int], ModuleType]

    def __init__(self, modules: Iterable[ModuleType]) -> None:
        self._modules_to_reload = set(modules)
        self._depth = 0

    @contextmanager
    def _stack_meter(self) -> Generator[int, None, None]:
        self._depth += 1
        yield self._depth
        self._depth -= 1

    def reload(self, module: ModuleType) -> None:
        try:
            self._modules_to_reload.remove(module)
        except KeyError:
            return

        with self._stack_meter():
            imp.reload(module)

    def __import__(  # type: ignore
        self,
        name: str,
        globals: Scope = None,
        locals: Scope = None,
        fromlist: Tuple[str] = (),
        level: int = 0
    ) -> ModuleType:
        module = self._orig___import__(name, globals, locals, fromlist, level)  # type: ignore

        self.reload(module)

        if fromlist:
            from_names = [
                name
                for item in fromlist
                for name in (
                    public_members(module) if item == '*' else [item]
                )
            ]

            for name in from_names:
                value = getattr(module, name, None)
                if ismodule(value):
                    self.reload(value)

        return module

    def __enter__(self) -> Callable[[ModuleType], None]:
        self._orig___import__ = __import__  # type: ignore
        builtins.__import__ = self.__import__  # type: ignore

        return self.reload

    def __exit__(self, exc_type: type, exc_value: Exception, traceback: TracebackType) -> None:
        builtins.__import__ = self._orig___import__  # type: ignore
        del self._orig___import__  # type: ignore
