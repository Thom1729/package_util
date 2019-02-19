def public_members(module):
    try:
        return module.__all__  # If not iterable, imports will break.
    except AttributeError:
        return [name for name in dir(module) if not name.startswith('_')]


def module_paths(module):
    try:
        yield module.__file__
    except AttributeError:
        pass

    try:
        yield from module.__path__
    except AttributeError:
        pass
