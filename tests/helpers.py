from sublime_lib import ResourcePath
from packages_util import TemporaryPackage

FIXTURES_PATH = ResourcePath.from_file_path(__file__).parent / 'fixtures'


def package_fixture(fixture):
    return TemporaryPackage(prefix=fixture, copy_from=FIXTURES_PATH / fixture)
