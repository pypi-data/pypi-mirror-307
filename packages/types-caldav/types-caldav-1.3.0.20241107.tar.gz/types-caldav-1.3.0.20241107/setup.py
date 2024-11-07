from setuptools import setup

name = "types-caldav"
description = "Typing stubs for caldav"
long_description = '''
## Typing stubs for caldav

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`caldav`](https://github.com/python-caldav/caldav) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `caldav`. This version of
`types-caldav` aims to provide accurate annotations for
`caldav==1.3.*`.

*Note:* The `caldav` package includes type annotations or type stubs
since version 1.4.0. Please uninstall the `types-caldav`
package if you use this or a newer version.


This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/caldav`](https://github.com/python/typeshed/tree/main/stubs/caldav)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.388,
and pytype 2024.10.11.
It was generated from typeshed commit
[`b674bfaebfdaf74f9e48cdeef1b1e800e28b2c30`](https://github.com/python/typeshed/commit/b674bfaebfdaf74f9e48cdeef1b1e800e28b2c30).
'''.lstrip()

setup(name=name,
      version="1.3.0.20241107",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/caldav.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-requests', 'types-vobject'],
      packages=['caldav-stubs'],
      package_data={'caldav-stubs': ['__init__.pyi', 'davclient.pyi', 'elements/__init__.pyi', 'elements/base.pyi', 'elements/cdav.pyi', 'elements/dav.pyi', 'elements/ical.pyi', 'lib/__init__.pyi', 'lib/error.pyi', 'lib/namespace.pyi', 'lib/url.pyi', 'lib/vcal.pyi', 'objects.pyi', 'requests.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
