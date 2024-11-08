#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Collect AWS Security Group details from multiple accounts."""

from ..helpers import helper_aws_ec2
from ..helpers import helper_common
from ..helpers import helper_aws_entrypoint
from ..helpers.helper_parameters import *
from multithreader import threads


def aws_sgs_get():
    """Collect AWS Security Group details."""
    # Enter AWS environment.
    session = helper_aws_entrypoint.auth()
    account_ids = helper_aws_entrypoint.crawler(session)

    # Execute task with multithreading.
    items = {
        'session': session,
        'assumed_role_name': assumed_role_name,
        'external_id': external_id,
        'region': region
    }
    results = threads(
        helper_aws_ec2.get_sgs,
        account_ids,
        items
    )

    # Convert results to CSV data and write to file.
    csv_data = helper_common.dicts_to_csv(results)
    helper_common.export_csv(csv_data, sgs_get_output_file)


def main():
    """Execute main function."""
    aws_sgs_get()


if __name__ == '__main__':
    main()
