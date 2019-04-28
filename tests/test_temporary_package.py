from unittest import TestCase

from sublime_lib import ResourcePath
from package_util import TemporaryPackage


class TestTemporaryPackage(TestCase):

    def test_temporary_package_name(self):
        expected_resource_path = ResourcePath('Packages/TemporaryPackageTest')
        expected_file_path = expected_resource_path.file_path()

        name = 'TemporaryPackageTest'
        with TemporaryPackage(name) as path:
            self.assertEquals(path.name, name)
            self.assertEquals(path, expected_resource_path)
            self.assertTrue(expected_file_path.is_dir())

        self.assertFalse(expected_file_path.exists())

    def test_temporary_package_prefix_suffix(self):
        prefix = 'TemporaryPackage'
        suffix = 'Test'
        with TemporaryPackage(prefix=prefix, suffix=suffix) as path:
            self.assertTrue(path.name.startswith(prefix))
            self.assertTrue(path.name.endswith(suffix))

    def test_temporary_package_arguments_error(self):
        with self.assertRaises(ValueError):
            TemporaryPackage('TemporaryPackageTest', prefix='foo')

        with self.assertRaises(ValueError):
            TemporaryPackage('TemporaryPackageTest', suffix='foo')

    def test_temporary_package_exclusive(self):
        with TemporaryPackage('TemporaryPackageTest'):
            with self.assertRaises(FileExistsError):
                with TemporaryPackage('TemporaryPackageTest'):
                    pass
