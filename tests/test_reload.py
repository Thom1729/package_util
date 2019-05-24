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

            for filename in ['foo.py', 'xyzzy.py']:
                file_path = path.joinpath('src', filename).file_path()
                file_path.with_name(filename + '.after_1').replace(file_path)

            reload_packages({path.package})

            self.assertEqual(module.FOO, 2)
            self.assertEqual(module.BAR, 2)

    def test_remove_module(self):
        with package_fixture('ReloadTest') as path:
            module = import_module(path.package + '.src.foo')

            self.assertEqual(module.FOO, 1)
            self.assertEqual(module.BAR, 1)

            for filename in ['foo.py']:
                file_path = path.joinpath('src', filename).file_path()
                file_path.with_name(filename + '.after_2').replace(file_path)

            path.joinpath('src', 'xyzzy.py').file_path().unlink()

            reload_packages({path.package})

            self.assertEqual(module.FOO, 2)
