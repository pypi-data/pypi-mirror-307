#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Provide common AWS EC2 multithreaded functions."""

import aws_crawler
import boto3


def get_sgs(
    account_id: str,
    items: dict
) -> dict:
    """Get AWS Security Group details from an AWS account."""
    print(f'Working on {account_id}...')

    try:
        # Get auth credentials for each account.
        credentials = aws_crawler.get_credentials(
            items['session'],
            f'arn:aws:iam::{account_id}:role/{items["assumed_role_name"]}',
            items['external_id']
        )

        # Create AWS EC2 client.
        client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key'],
            aws_session_token=credentials['aws_session_token'],
            region_name=items['region']
        )
        response = client.describe_security_groups()

        # Get all Security Group details in the specified region.
        paginator = client.get_paginator('describe_security_groups')
        response_iterator = paginator.paginate()

        # Read through pages of Security Group details.
        sg_list = []
        for page in response_iterator:
            for sg in page['SecurityGroups']:
                sg_list.append(sg)

        # Process details.
        if sg_list == []:
            number_of_sgs = 0
            sgs = None
        else:
            number_of_sgs = len(sg_list)
            sgs = [sg['GroupId'] for sg in sg_list]

    # In case of any exceptions, return the error message but allow loop to continue.
    except Exception as e:
        number_of_sgs = str(e)
        sgs = None

    return {
        'account_id': account_id,
        'number_of_sgs': number_of_sgs,
        'details': sgs
    }


def main():
    """Execute main function."""
    pass


if __name__ == '__main__':
    main()
