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

It is an opinionated piece of software that fits some workflows better
than others. It reduces some boilerplate ``git`` commands to a
minimum. Probably most of it can be done with ``git`` aliases and
writing a longer ``hub`` command. Even in this early stage it is being
extensively dogfooded: try it out and provide feedback in `Issues`_.

.. _`arcanist`: https://github.com/phacility/arcanist
.. _`Issues`: https://github.com/seporaitis/warlok/issues


Example Story
-------------

Start working on a new feature branch, branching off of
``origin/master``.

.. code-block:: bash

    $ wlk feature new-feature

Behind the scenes this does:

.. code-block:: bash

    $ git fetch origin
    $ git stash
    $ git checkout origin/master
    $ git checkout -b new-feature
    $ git stash pop

Do some work and commit, and commit more - that's part of the fun!
Then:

.. code-block:: bash

    $ wlk push

Behind the scenes this does:

.. code-block:: bash

    $ git push origin new-feature
    $ hub pull-request -b master -h new-feature

You can continue doing work, committing and ``wlk push``-ing. Repeated
``wlk push`` calls just do ``git push origin new-feature``.

Create a another feature on top of ``new-feature``:

.. code-block:: bash

    $ wlk feature another-feature new-feature
    # do some work
    $ git commit -m "New changes."
    $ wlk push

Behind the scenes this does:

    $ git fetch origin
    $ git stash
    $ git checkout new-feature
    $ git checkout -b another-feature
    $ git stash pop
    # your changes come here
    $ git commit -m "New changes."
    $ git push origin another-feature
    $ hub pull-request -b new-feature -h another-feature

Note this still requires ``hub`` and setting of reviewers. The end
goal is:

* replace ``hub`` with direct API integration;
* set reviewers based on pull-request message;
* get rid of ``git commit`` step - ``wlk`` should pick up staged
  changes and commit them if necessary.

In the end leaving three commands:

.. code-block:: bash

    wlk feature
    wlk push
    wlk merge  (see below)


In The Future
-------------

Merging changes

.. code-block:: bash

    $ wlk merge new-feature

Behind the scenes - merges the pull request associated with
``new-feature``.

Undecided:

* should it find the sequence of pull-requests and merge the sequence
  backwards until finally ``new-feature`` gets merged into
  ``origin/master``?
* should it find the sequence of pull-requests and suggest merging
  them first?
* should it merge and inform about "orphaned" pull requests that have
  their base branch changed?


Checking code review status:

.. code-block:: bash

    $ wlk review

    Waiting on You:
      - #134    [review]   Changed some files.
      - #12     [approved] Implemented a feature.

    Waiting on Others:
      - #122    [review]   Hotfix a bug.
      - #44     [changes]  Implemented a big feature.


Limitations & Assumptions & Ideas
---------------------------------

* Limitation: Single remote
* Idea: Required/Optional fields
* Idea: Customization of fields via ``setup.cfg`` configuration
* Idea: Custom field handlers via ``setup.cfg`` configuration
* TBD
