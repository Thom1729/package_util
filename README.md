# package_util

A Sublime Text dependency for working with packages.

## Motivation

The primary purpose of package_util is to provide a common implementation of package reloading that consolidates the work that has been done on the subject in various places and provides a comprehensive test suite. Other functionality may be added in the future.

Thanks to:
- [randy3k](https://randycity.github.io/) for [AutomaticPackageReloader](https://github.com/randy3k/AutomaticPackageReloader), from which package_util's reloading logic was derived.
- [divmain](http://divmain.com/), for writing the “ancestral” reloading code for (GitSavvy)[https://github.com/divmain/GitSavvy].
- [wbond](https://wbond.net/) for writing [Package Control](https://packagecontrol.io) and for [adding `sublime_plugin.load_module` to the Sublime API](https://github.com/SublimeTextIssues/Core/issues/2590), which dramatically simplifies this implementation.

## Installation

To use package_util in your own package, declare it as a dependency of your package. Create a file named `dependencies.json` in the root of your package with the following contents:

```json
{
    "*": {
        "*": [
            "package_util",
            "sublime_lib"
        ]
    }
}
```

The implementation of package_util uses [sublime_lib](https://github.com/SublimeText/sublime_lib). At the present time, Package Control does not allow dependencies to depend on other dependencies, so you must declare a dependency on sublime_lib as well (as in the example `dependencies.json`).

## API

### def package_util.reload_packages(packages: Iterable[str])

Reload the given `packages`.

Example usage:

```python
from package_util import reload_packages

reload_packages({ 'MyPackage' })
```

If any of the given packages has dependents, those dependents are reloaded as well, and so on recursively. This behavior relies on [Package Control](https://packagecontrol.io/). If Package Control is not installed, then dependents will not be reloaded. At present, Package Control only supports package-dependency relationships and not package-package or dependency-dependency relationships. However, package_util will observe any dependency relationships declared in a `dependencies.json` file.

The reloading procedure is as follows:

1. Recursively find all packages and dependencies that depend on the given `packages`.
2. Find all loaded modules that belong to any of the above.
3. Tell Sublime to unload any plugins among those modules.
4. Reload all of the modules.
5. Tell Sublime to load any plugins among those modules.

### class TemporaryPackage(name: Optional[str], \*\*args)

A temporary Sublime Text package.

The constructor takes the following optional arguments:

<dl>
<dt>name</dt>
<dd>The name of the temporary package. This determines the name of the package directory, and Sublime will refer to the package by the given name. If no name is given, a random name will be generated.</dd>
<dt>prefix</dt>
<dd>A prefix to use for the randomly generated package name. Exclusive with the name argument.</dd>
<dt>prefix</dt>
<dd>A suffix to use for the randomly generated package name. Exclusive with the name argument.</dd>
<dt>copy_from</dt>
<dd>When the temporary package is initialized, copy files from the given resource path into the temporary package.</dd>
<dt>wrap_ignore</dt>
<dd>When the temporary package is initialized or cleaned up, ignore the temporary package. This ensures the package is not visible in an incomplete state. This option is true by default.</dd>
</dl>

The temporary package is not created automatically; you must call the `init()` method. TemporaryPackage can also be used as a context manager, wrapping the contents with the `init()` and `cleanup()` methods.

#### def init()

Create the temporary package in the filesystem. If the `copy_from` constructor argument was given, then copy resources from that path. If the `wrap_ignore` constructor argument was given, then add the temporary package to the ignored packages list while the method is in progress.

#### def cleanup()

Remove the temporary package in the filesystem. If the `wrap_ignore` constructor argument was given, then add the temporary package to the ignored packages list while the method is in progress.
