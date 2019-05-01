from unittest import TestCase
from types import ModuleType

from package_util.util.dependencies import get_dependents
from package_util.util.module_utils import public_members, module_paths


def mock_module(name, members):
    module = ModuleType(name)

    module.__doc__ = None
    module.__loader__ = None

    for key, value in members.items():
        setattr(module, key, value)

    return module


class TestUtils(TestCase):
    def test_dependency_resolution(self):
        dependency_relationships = [
            ('a', 'b'),
            ('a', 'c'),
            ('b', 'd'),
            ('c', 'd'),
            ('x', 'y'),
        ]

        for initial, result in [
            (set(), set()),
            ({'a'}, {'a'}),
            ({'b'}, {'a', 'b'}),
            ({'d'}, {'a', 'b', 'c', 'd'}),
            ({'e'}, {'e'}),
        ]:
            self.assertEqual(
                get_dependents(initial, dependency_relationships),
                result
            )

    def test_public_members(self):
        for module, result in [
            (
                mock_module('empty', {}),
                set()
            ),
            (
                mock_module('auto', {
                    'a': 1,
                    'b': 1,
                    '_c': 1,
                    '__d__': 1,
                }),
                {'a', 'b'}
            ),
            (
                mock_module('all', {
                    'a': 1,
                    'b': 1,
                    '_c': 1,
                    '__d__': 1,
                    '__all__': ['b', '_c', 'x'],
                }),
                {'b', '_c', 'x'}
            ),
        ]:
            self.assertEqual(
                set(public_members(module)),
                result
            )

    def test_module_paths(self):
        for module, result in [
            (
                mock_module('empty', {}),
                set()
            ),
            (
                mock_module('file', {
                    '__file__': 'a',
                }),
                {'a'}
            ),
            (
                mock_module('path', {
                    '__path__': ['x', 'y', 'z'],
                }),
                {'x', 'y', 'z'}
            ),
            (
                mock_module('both', {
                    '__file__': 'a',
                    '__path__': ['x', 'y', 'z'],
                }),
                {'a', 'x', 'y', 'z'}
            ),
        ]:
            self.assertEqual(
                set(module_paths(module)),
                result
            )
