import sublime

from contextlib import contextmanager


@contextmanager
def ignore_package(name):
    preferences = sublime.load_settings('Preferences.sublime-settings')

    ignored = preferences.get("ignored_packages").copy()
    already_ignored = (name in ignored)
    if not already_ignored:
        ignored.append(name)
        preferences.set("ignored_packages", ignored)

    yield

    if not already_ignored:
        ignored = preferences.get("ignored_packages").copy()
        if name in ignored:
            ignored.remove(name)
            preferences.set("ignored_packages", ignored)