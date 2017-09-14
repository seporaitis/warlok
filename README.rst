======
warlok
======

.. image:: https://img.shields.io/pypi/v/warlok.svg
        :target: https://pypi.python.org/pypi/warlok

.. image:: https://img.shields.io/travis/seporaitis/warlok/master.svg
        :target: https://travis-ci.org/seporaitis/warlok

.. image:: https://readthedocs.org/projects/warlok/badge/?version=latest
        :target: http://warlok.readthedocs.io/en/latest/?badge=latest


Warlok - an evil cousin to `arcanist`_. A command-line tool for GitHub.

.. _`arcanist`: https://github.com/phacility/arcanist

Commands
--------

* ``wlk feature feature-name [base]`` - branch off for new feature
* ``wlk push`` - push feature for review
* ``wlk pull`` - pull a pull request locally
* ``wlk review`` - list assigned pull requests
* ``wlk review 10`` - open pull request #10 for review


Example Workflow
----------------

Starting off a pull request:

.. code-block:: bash

    $ wlk feature new-feature
    # change some files
    $ git commit -m "Changed some files"
    $ wlk push


Continuing changes:

.. code-block:: bash

    $ git commit -m "More changes"
    $ wlk push


Checking code review status:

.. code-block:: bash

    $ wlk review

    Waiting on You:
      - #134    [review]   Changed some files.
      - #12     [approved] Implemented a feature.

    Waiting on Others:
      - #122    [review]   Hotfix a bug.
      - #44     [changes]  Implemented a big feature.


Limitations & Assumptions
-------------------------

* Single remote
* TBD
