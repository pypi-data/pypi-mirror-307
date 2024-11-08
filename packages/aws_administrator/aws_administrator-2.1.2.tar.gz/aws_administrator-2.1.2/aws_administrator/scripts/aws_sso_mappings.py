#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Update AWS SSO mappings data with new principals."""

from ..helpers import helper_aws_sso
from ..helpers import helper_common
from ..helpers.helper_parameters import *


def aws_sso_mappings():
    """Update AWS SSO mappings data with new principals."""
    # Read CSV file with new identity mappings.
    data = helper_common.read_csv(
        sso_mappings_map_file
    )

    # Process JSON data to update to new identities.
    mappings = helper_aws_sso.process_mappings(
        data,
        sso_mappings_input_file,
        sso_mappings_old_user_heading,
        sso_mappings_new_user_heading,
        sso_mappings_old_group_pattern,
        sso_mappings_new_group_pattern
    )

    # Write updated principals JSON file.
    helper_common.write_json_str(
        sso_mappings_output_file,
        mappings
    )


def main():
    """Execute main function."""
    aws_sso_mappings()


if __name__ == '__main__':
    main()
