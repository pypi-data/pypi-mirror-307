=====================
**aws_administrator**
=====================

Overview
--------

Run AWS administrative scripts. Available scripts are in in the package's "scripts" directory: https://gitlab.com/fer1035_python/modules/pypi-aws_administrator/-/tree/main/src/aws_administrator/scripts (see each script's docstring for more information).

Usage
------

Installation:

.. code-block:: BASH

    pip3 install aws_administrator
    # or
    python3 -m pip install aws_administrator

Prerequisite steps:

1. Copy the "parameters.ini" file: https://gitlab.com/fer1035_python/modules/pypi-aws_administrator/-/blob/main/src/aws_administrator/extras/parameters.ini to your current working directory.

2. Update the file with the necessary values.

Example (Python shell):

.. code-block:: PYTHON

    # Get AWS SSO Permission Set details from all accounts in an organization.

    from aws_administrator.scripts import aws_sso_get
    aws_sso_get.aws_sso_get()

Notes
-----

These scripts arose from the needs of my work to migrate AWS SSO and security details from one organization to another. There's the long way of doing it, then there's the easy way (recommended). Both are covered by the scripts.

In the process, I have decided to modularize and release them as a package of reusable functions. The functions are available in the package's "helpers" directory: https://gitlab.com/fer1035_python/modules/pypi-aws_administrator/-/tree/main/src/aws_administrator/helpers (as with the scripts, see each helper's docstring for more information). The parameters have also been abstracted so that the scripts themselves can be used with very few customizations, if any.
