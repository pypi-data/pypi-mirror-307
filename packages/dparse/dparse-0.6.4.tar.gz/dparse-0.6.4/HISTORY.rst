=======
History
=======

0.6.3 (2023-06-26)
------------------

* Use the modern tomli/tomllib to parse TOML files. (thanks @mgorny)
* Drop Python 3.5 from our CI.

0.6.2 (2022-09-19)
------------------

* Fixed bug: always call the parent from the PATH in the resolve_file function.

0.6.1 (2022-09-19)
------------------

* Fixed a bug in the resolve_file function.

0.6.0 (2022-09-09)
------------------

* Adds support for parsing poetry.lock files
* Adds a way to resolve all the linked dependencies in one Dependency File
* Throws exceptions if found in the parsing process (This may be a breaking change)

0.5.2 (2022-08-09)
------------------

* Install pyyaml only when asked for with extras (conda extra)
* Add support for piptools requirements.in
* Use ConfigParser directly
* Removed a regex used in the index server validation, fixing a possible ReDos security issue

0.5.1 (2020-04-26)
------------------

* Fixed package metadata removing 2.7 support
* Install pipenv only when asked for with extras

0.5.0 (2020-03-14)
------------------

A bug with this package allows it to be installed on Python 2.7 environments,
even though it should not work on such version. You should stick with version
0.4.1 version instead for Python 2.7 support.

* Dropped Python 2.7, 3.3, 3.4 support
* Removed six package
* Removed pinned dependencies of tests
* Dropped setup.py tests support in favor of tox

0.4.1 (2018-04-06)
------------------

* Fixed a packaging error.

0.4.0 (2018-04-06)
------------------

* pipenv is now an optional dependency that's only used when updating a Pipfile. Install it with dparse[pipenv]
* Added support for invalid toml Pipfiles (thanks @pombredanne)


0.3.0 (2018-03-01)
------------------

* Added support for setup.cfg files (thanks @kexepal)
* Dependencies from Pipfiles now include the section (thanks @paulortman)
* Multiline requirements are now ignored if they are marked
* Added experimental support for Pipfiles

0.2.1 (2017-07-19)
------------------

* Internal refactoring

0.2.0 (2017-07-19)
------------------

* Removed setuptools dependency


0.1.1 (2017-07-14)
------------------

* Fixed a bug that was causing the parser to throw errors on invalid requirements.

0.1.0 (2017-07-11)
------------------

* Initial, not much to see here.
