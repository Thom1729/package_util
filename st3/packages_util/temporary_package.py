from os import mkdir
from shutil import rmtree

from sublime_lib import ResourcePath

from .ignore_package import ignore_package
from .util.null_contextmanager import null_contextmanager
from .util.random import random_token


class TemporaryPackage():
    def __init__(
        self, name=None,
        *,
        prefix=None, suffix=None,
        copy_from=None, wrap_ignore=True
    ):
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

    def __enter__(self):
        self.init()
        return self.path

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def _ignore(self):
        if self.wrap_ignore:
            return ignore_package(self._name)
        else:
            return null_contextmanager()

    def init(self):
        with self._ignore():
            if self.copy_from is None:
                mkdir(str(self.path.file_path()))
            else:
                ResourcePath(self.copy_from).copytree(self.path.file_path())

    def cleanup(self):
        with self._ignore():
            rmtree(str(self.path.file_path()))
