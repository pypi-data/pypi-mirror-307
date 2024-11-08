#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Assign AWS SSO Permission Sets to multiple accounts."""

from ..helpers import helper_aws_sso
from ..helpers import helper_common
from ..helpers import helper_aws_entrypoint
from ..helpers.helper_parameters import *
from multithreader import threads
from pprint import pprint as pp


def aws_sso_assign():
    """Assign AWS SSO Permission Sets."""
    # Enter AWS environment.
    session = helper_aws_entrypoint.auth()
    sso_admin = session.client(
        'sso-admin',
        region_name=region
    )

    # Create accounts list from JSON file.
    data = helper_common.read_json(sso_assign_input_file)
    account_ids = [account['account_id'] for account in data]

    # Execute task with multithreading.
    items = {
        'sso_admin': sso_admin,
        'sso_instance_arn': sso_instance_arn,
        'data': data
    }
    results = threads(
        helper_aws_sso.assign_permission_sets_dry_run,
        account_ids,
        items
    ) if DRY_RUN else threads(
        helper_aws_sso.assign_permission_sets,
        account_ids,
        items
    )

    # Print results.
    pp(results)


def main():
    """Execute main function."""
    aws_sso_assign()


if __name__ == '__main__':
    main()
