from importlib import import_module
from unittest import TestCase

from sublime_lib import ResourcePath
from package_util import reload_packages, TemporaryPackage

FIXTURES_PATH = ResourcePath.from_file_path(__file__).parent / 'fixtures'


def package_fixture(fixture):
    return TemporaryPackage(prefix=fixture, copy_from=FIXTURES_PATH / fixture)


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

            reload_packages({path.package})

            self.assertEqual(module.FOO, 2)
            self.assertEqual(module.BAR, 2)
