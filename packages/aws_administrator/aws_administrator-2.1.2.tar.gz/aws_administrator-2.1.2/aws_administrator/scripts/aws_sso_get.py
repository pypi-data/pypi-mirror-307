#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Collect AWS SSO Permission Set assignment data from multiple accounts."""

from ..helpers import helper_aws_sso
from ..helpers import helper_common
from ..helpers import helper_aws_entrypoint
from ..helpers.helper_parameters import *
from multithreader import threads


def aws_sso_get():
    """Collect AWS SSO Permission Set assignment data."""
    # Enter AWS environment.
    session = helper_aws_entrypoint.auth()
    account_ids = helper_aws_entrypoint.crawler(session)
    sso_admin = session.client(
        'sso-admin',
        region_name=region
    )
    identity_store = session.client(
        'identitystore',
        region_name=region
    )

    # Execute task with multithreading.
    items = {
        'sso_admin': sso_admin,
        'identity_store': identity_store,
        'sso_instance_arn': sso_instance_arn,
        'identity_store_id': identity_store_id
    }
    results = threads(
        helper_aws_sso.get_permission_sets,
        account_ids,
        items
    )

    # Write results to file.
    helper_common.write_json_dict(
        sso_get_output_file,
        results
    )


def main():
    """Execute main function."""
    aws_sso_get()


if __name__ == '__main__':
    main()
