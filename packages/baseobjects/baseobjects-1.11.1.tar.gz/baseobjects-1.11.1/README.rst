baseobjects
============

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/baseobjects.svg
   :target: https://pypi.org/project/baseobjects/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/baseobjects.svg
   :target: https://pypi.org/project/baseobjects/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/baseobjects
   :target: https://pypi.org/project/baseobjects
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/baseobjects
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/python-baseobjects/latest.svg?label=Read%20the%20Docs
   :target: https://python-baseobjects.readthedocs.io/
   :alt: Read the documentation at https://python-baseobjects.readthedocs.io/
.. |Tests| image:: https://github.com/fongant/python-baseobjects/workflows/Tests/badge.svg
   :target: https://github.com/fongant/baseobjects/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/fongant/python-baseobjects/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/fongant/python-baseobjects
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

This package contains useful base objects meant for inheritance and helper functions.

* bases: Low level base classes.

* cachingtools: Objects and decorators for local caching.
* collections: Objects for storing other objects.
* composition: Objects for creating compositions style objects.
* dataclasses: Objects for storing information efficiently.
* functions: Objects for creating function and method objects.
* metaclasses: Base metaclasses.
* objects: Uncategorized base objects.
* operations: An assortment functions for doing specific.
* typing: Objects to be used when adding typing to python code.
* versioning: Objects for tracking versions.
* wrappers: Objects for wrapping other objects.

Requirements
------------

* Python 3.10 or later
* bidict
* click


Installation
------------

You can install *baseobjects* via pip_ from PyPI_:

.. code:: console

   $ pip install baseobjects


Usage
-----

Please see the `Command-line Reference <Usage_>`_ for details.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*baseobjects* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/fongant/python-baseobjects/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://python-baseobjects.readthedocs.io/en/latest/usage.html
