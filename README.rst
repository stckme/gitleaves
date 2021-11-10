==========
git leaves
==========
Git Based Leaves management system

Project status: WIP
~~~~~~~~~~~~~~~~~~~~

.. image:: https://img.shields.io/pypi/v/gitleaves.svg
        :target: https://pypi.python.org/pypi/gitleaves

.. image:: https://img.shields.io/travis/shon/gitleaves.svg
        :target: https://travis-ci.com/shon/gitleaves

.. image:: https://readthedocs.org/projects/gitleaves/badge/?version=latest
        :target: https://gitleaves.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/shon/gitleaves/shield.svg
     :target: https://pyup.io/repos/github/shon/gitleaves/
     :alt: Updates



* Free software: MIT license
* Documentation: https://gitleaves.readthedocs.io.

Specifications
---------------
File names
~~~~~~~~~~
- leaves.\<YYYY\>.csv
- extras.\<YYYY\>.csv

Format
~~~~~~~~~~

**Leaves**
MMDD [- MMDD], Name, Reason / Details [Optional]

**Extra days**
MMDD [- MMDD], Name, Reason / Details [Optional]

**Example**

.. code-block:: csv
    1115 - 1126, Tony Stark, Hawaii
    1129 - 1210, Peter Parker,
    1129 - 1202, Bruce Wayne,
    1220 - 1224, Loki Laufeyson, Smell the flowers


Process
~~~~~~~~~~
- Apply for leave(s) by adding records to leaves.YYYY.csv
- Optionally mention details/reasons in commit message
- Raise a PR
- Leave is approved if the PR is merged

Guidelines
~~~~~~~~~~~
- Do take leaves when necessary :)
- Make sure you spell your name same everywhere
- Generally try to add records in order
- When applying for leaves
    - make sure you take look at peers leave plans 
    - ensure that you have a collegue to cover your work while you are away
    - if necessary, do essential knowledge transfer to ensure that there are no dependencies on you
    - if you are a major contributor to an important release then avoid immediate leaves after the release

Dev Guidelines
~~~~~~~~~~~~~~
- Human Readable data files (as much possible)

Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
