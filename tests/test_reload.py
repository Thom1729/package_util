from importlib import import_module
from unittest import TestCase

from packages_util.reloader import reload_package

from .helpers import package_fixture


class TestReload(TestCase):
    def test_reload_a(self):
        with package_fixture('ReloadTest') as path:
            module = import_module(path.package + '.src.foo')

            self.assertEqual(module.FOO, 1)
            self.assertEqual(module.BAR, 1)

            with path.joinpath('src/foo.py').file_path().open('a') as file:
                file.write('FOO = 2\n')

            with path.joinpath('src/xyzzy.py').file_path().open('a') as file:
                file.write('BAR = 2\n')

            reload_package(path.package)

            self.assertEqual(module.FOO, 2)
            self.assertEqual(module.BAR, 2)
