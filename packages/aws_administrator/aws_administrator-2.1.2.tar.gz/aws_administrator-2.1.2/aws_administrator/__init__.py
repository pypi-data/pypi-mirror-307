#!/usr/bin/env python3
# -*- coding: latin-1 -*-

"""
Run AWS administrative scripts.

Available scripts can be found in the
'scripts' directory of this package.

Prerequisite steps:
1. Copy the extras/parameters.ini file to your current working directory.
2. Update the file with the necessary values.

Example usage:
from aws_administrator.scripts import aws_sso_get
aws_sso_get.aws_sso_get()
"""


__version__ = '2.1.2'
__author__ = 'Ahmad Ferdaus Abd Razak'
__status__ = 'Production'
