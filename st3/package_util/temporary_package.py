from os import mkdir
from shutil import rmtree
from contextlib import ExitStack

from sublime_lib import ResourcePath

from .ignore_package import ignore_package
from .util.random import random_token

from types import TracebackType
from .compat.typing import ContextManager, Optional


class TemporaryPackage():
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        copy_from: Optional[str] = None,
        wrap_ignore: bool = True
    ) -> None:
        if name is None:
            self._name = '{prefix}{token}{suffix}'.format(
                prefix=prefix or '',
                token=random_token(),
                suffix=suffix or '',
            )
        elif prefix is not None or suffix is not None:
            raise ValueError("Argument `name` is incompatible with `prefix` and `suffix`.")
        else:
            self._name = name

        self.copy_from = copy_from
        self.wrap_ignore = wrap_ignore

        self.path = ResourcePath('Packages', self._name)

    def __enter__(self) -> ResourcePath:
        self.init()
        return self.path

    def __exit__(self, exc_type: type, exc_value: Exception, traceback: TracebackType) -> None:
        self.cleanup()

    def _ignore(self) -> ContextManager:
        ret = ExitStack()
        if self.wrap_ignore:
            ret.enter_context(ignore_package(self._name))
        return ret

    def init(self) -> None:
        with self._ignore():
            if self.copy_from is None:
                mkdir(str(self.path.file_path()))
            else:
                ResourcePath(self.copy_from).copytree(self.path.file_path())

    def cleanup(self) -> None:
        with self._ignore():
            rmtree(str(self.path.file_path()))
