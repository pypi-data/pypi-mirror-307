# docplex-extensions

[![license](https://img.shields.io/pypi/l/docplex-extensions.svg)](https://github.com/samarthmistry/docplex-extensions/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/docplex-extensions.svg)](https://pypi.python.org/pypi/docplex-extensions)
[![pyversions](https://img.shields.io/pypi/pyversions/docplex-extensions.svg)](https://pypi.python.org/pypi/docplex-extensions)

[![CI](https://github.com/samarthmistry/docplex-extensions/actions/workflows/ci.yaml/badge.svg)](https://github.com/samarthmistry/docplex-extensions/blob/main/.github/workflows/ci.yaml)
[![Tests](https://github.com/samarthmistry/docplex-extensions/actions/workflows/tests.yaml/badge.svg)](https://github.com/samarthmistry/docplex-extensions/blob/main/.github/workflows/tests.yaml)
[![Coverage](coverage.svg)](https://github.com/samarthmistry/docplex-extensions/blob/main/coverage.svg)

A collection of custom data structures and user-friendly functions for mathematical optimization modeling with [DOcplex — IBM® Decision Optimization CPLEX® Modeling for Python](http://ibmdecisionoptimization.github.io/docplex-doc).

Features
--------

* **Specialized data structures**: For defining index-sets, parameters, and decision variables — enabling concise and high-performance algebraic modeling.
* **Easy access to additional CPLEX functionality**: Like [displaying problem statistics](https://www.ibm.com/docs/en/icos/22.1.1?topic=problem-displaying-statistics) and [displaying solution quality statistics](https://www.ibm.com/docs/en/icos/22.1.1?topic=cplex-evaluating-solution-quality) — not directly available in DOcplex.
* **Type-complete interface**: Enables static type checking and intelligent auto-completion suggestions with modern IDEs — reducing type errors and improving development speed.
* **Robust codebase**: 100% coverage spanning 1500+ test cases and fully type-checked with mypy under [strict mode](https://mypy.readthedocs.io/en/stable/getting_started.html#strict-mode-and-configuration).

Links
-----

* [Documentation](https://docplex-extensions.readthedocs.io/en/stable)
* [Installation](https://docplex-extensions.readthedocs.io/en/stable/installation.html)
* [Source code](https://github.com/samarthmistry/docplex-extensions)
* [Changelog](https://github.com/samarthmistry/docplex-extensions/releases)

Development
-----------

Dev dependencies can be installed with the pip [extras](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-extras) `dev`.

* Create HTML documentation locally with: `docs/make html`.
* Run unit tests and functional tests with: `pytest tests`.
* Run doctests with: `pytest src`.
* Run static typing tests with: `mypy tests/typing_tests`.

License
-------

*docplex-extensions* is an open-source project developed by [Samarth Mistry](https://www.linkedin.com/in/samarthmistry) and released under the Apache 2.0 License. See the [LICENSE](https://github.com/samarthmistry/docplex-extensions/blob/main/LICENSE) and [NOTICE](https://github.com/samarthmistry/docplex-extensions/blob/main/NOTICE) for more details.
