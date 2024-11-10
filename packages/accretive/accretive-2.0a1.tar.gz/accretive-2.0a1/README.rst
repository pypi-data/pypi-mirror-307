.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+

*******************************************************************************
                                  accretive
*******************************************************************************

.. image:: https://img.shields.io/pypi/v/accretive
   :alt: Project Version
   :target: https://pypi.org/project/accretive/

.. image:: https://img.shields.io/pypi/status/accretive
   :alt: PyPI - Status
   :target: https://pypi.org/project/accretive/

.. image:: https://github.com/emcd/python-accretive/actions/workflows/tester.yaml/badge.svg?branch=master&event=push
   :alt: Tests Status
   :target: https://github.com/emcd/python-accretive/actions/workflows/tester.yaml

.. image:: https://emcd.github.io/python-accretive/coverage.svg
   :alt: Code Coverage Percentage
   :target: https://github.com/emcd/python-accretive/actions/workflows/tester.yaml

.. image:: https://img.shields.io/pypi/pyversions/accretive
   :alt: Python Versions
   :target: https://pypi.org/project/accretive/

.. image:: https://img.shields.io/pypi/l/accretive
   :alt: Project License
   :target: https://github.com/emcd/python-accretive/blob/master/LICENSE.txt

A Python library package which provides *accretive data structures*.

Accretive data structures can grow at any time but can never shrink. An
accretive dictionary accepts new entries, but cannot have existing entries
altered or removed. Similarly, an accretive namespace accepts new attributes,
but cannot have existing attributes assigned to new values or deleted.

Accretive data structures are useful as registries, which may be incrementally
initialized, but should have immutable state, once initialized. In general,
they are a good compromise between the safety of immutability and the
convenience of incremental initialization.

.. note::

    Enforcement of immutability is quite difficult in Python. While this
    library encourages immutability by default, it can be circumvented by
    anyone who has intermediate knowledge of Python machinery and who is
    determined to circumvent the immutability. Use the library in the spirit of
    making programs safer, but understand that it cannot truly prevent unwanted
    state tampering.

In addition to accretive **dictionaries** (including dictionaries with *default
entries*) and **namespaces**, this package also provides accretive **classes**
(including *abstract base classes*), **modules**, and **objects**. Subpackages
provide variants of all of these with some additional behaviors or constraints.
Modules of aliases are also provided to satisfy various import styles and
nomenclatural conventions.


Examples
===============================================================================


Accretive Namespace
-------------------------------------------------------------------------------

An accretive namespace, similar to ``types.SimpleNamespace``, is available.
This namespace can be initialized from multiple iterables and from keyword
arguments. (Keyword arguments shown below; see documentation for additional
forms of initialization.)

>>> from accretive import Namespace
>>> ns = Namespace( apples = 12, bananas = 6, cherries = 42 )
>>> ns
accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42 )

Arbitrary attributes can be assigned, as is expected in Python.

>>> ns.blueberries = 96
>>> ns.strawberries = 24
>>> ns
accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42, blueberries = 96, strawberries = 24 )

Since the namespace is accretive, attributes cannot be deleted.

>>> del ns.apples
Traceback (most recent call last):
...
accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'apples'.

Or reassigned.

>>> ns.apples = 14
Traceback (most recent call last):
...
accretive.exceptions.IndelibleAttributeError: Cannot reassign or delete existing attribute 'apples'.

The attributes thus retain their original values.

>>> ns
accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42, blueberries = 96, strawberries = 24 )


Accretive Dictionary
-------------------------------------------------------------------------------

An accretive dictionary, similar to ``dict``, is available. This dictionary can
be initialized from multiple iterables and from keyword arguments. (Keyword
arguments shown below; see documentation for additional forms of
initialization.)

>>> from accretive import Dictionary
>>> dct = Dictionary( apples = 12, bananas = 6, cherries = 42 )
>>> dct
accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42} )

Entries can be added to the dictionary after initialization. This includes via
a batch operation, such as ``update``, which can accept the same forms of
arguments as dictionary initialization.

>>> dct.update( blueberries = 96, strawberries = 24 )
accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42, 'blueberries': 96, 'strawberries': 24} )

Since the dictionary is accretive, existing entries cannot be removed.

>>> del dct[ 'bananas' ]
Traceback (most recent call last):
...
accretive.exceptions.IndelibleEntryError: Cannot update or remove existing entry for 'bananas'.

Or altered.

>>> dct[ 'bananas' ] = 11
Traceback (most recent call last):
...
accretive.exceptions.IndelibleEntryError: Cannot update or remove existing entry for 'bananas'.

The entries thus remain unchanged.

>>> dct
accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42, 'blueberries': 96, 'strawberries': 24} )


Installation
===============================================================================

::

    pip install accretive


`More Flair <https://www.imdb.com/title/tt0151804/characters/nm0431918>`_
===============================================================================
...than the required minimum

.. image:: https://img.shields.io/github/last-commit/emcd/python-accretive
   :alt: GitHub last commit
   :target: https://github.com/emcd/python-accretive

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
   :alt: Hatch
   :target: https://github.com/pypa/hatch

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :alt: pre-commit
   :target: https://github.com/pre-commit/pre-commit

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
   :alt: Bandit
   :target: https://github.com/PyCQA/bandit

.. image:: https://www.mypy-lang.org/static/mypy_badge.svg
   :alt: Mypy
   :target: https://mypy-lang.org

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
   :alt: Pylint
   :target: https://github.com/pylint-dev/pylint

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :alt: Ruff
   :target: https://github.com/astral-sh/ruff

.. image:: https://img.shields.io/pypi/implementation/accretive
   :alt: PyPI - Implementation
   :target: https://pypi.org/project/accretive/

.. image:: https://img.shields.io/pypi/wheel/accretive
   :alt: PyPI - Wheel
   :target: https://pypi.org/project/accretive/
