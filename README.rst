Rent or Own
===========

A rent or own calculator based to the best of my abilities on Canadian data.

|Tests| |Codecov|

|pre-commit| |Black|

.. |Tests| image:: https://github.com/ianepreston/rentorown/workflows/Tests/badge.svg
   :target: https://github.com/ianepreston/rentorown/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/ianepreston/rentorown/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ianepreston/rentorown
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/ianepreston/rentorown/HEAD?urlpath=lab&filepath=index.ipynb
   :alt: Binder


IMPORTANT DISCLAIMER
--------------------

The calculations and results of this code are presented without any warranty. Don't make
a huge financial decision based off some code you found on the internet. While I've done
my best to make a good model, I've made a number of assumptions about the structure
of the problem. On top of that, the model itself requires entering a number of assumptions.
The model can only be said to be accurate if the calculations are correct, the structure
of the problem is correct, and the assumptions that the user enters to specify their exact
comparison are correct. I made this as a model to organize my thinking about the tradeoffs
of renting vs owning a home, and have made efforts to make it accurate, but I can't offer
any guarantees to its validity, and assume no responsibility for any financial decisions
anyone might make in whole or in part due to its results. Hope that covers my ass.


Installation
------------

You can install *Rent or Own* with poetry:

.. code:: console

   $ git clone https://github.com/ianepreston/rentorown.git
   $ cd rentorown
   $ poetry install



License
-------

Distributed under the terms of the `GPL 3.0 license`_,
*Rent or Own* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _GPL 3.0 license: https://opensource.org/licenses/GPL-3.0
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/ianepreston/rentorown/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://rentorown.readthedocs.io/en/latest/usage.html
