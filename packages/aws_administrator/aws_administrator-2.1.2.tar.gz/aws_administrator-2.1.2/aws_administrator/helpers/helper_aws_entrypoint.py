#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Provide AWS auth and crawler options."""

from .helper_parameters import *
import aws_crawler
from aws_authenticator import AWSAuthenticator as awsauth


def auth():
    """Login to AWS."""
    if auth_method == 'profile':
        auth = awsauth(
            profile_name=profile_name,
        )
        session = auth.profile()
    elif auth_method == 'iam':
        auth = awsauth(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
        )
        session = auth.iam()
    elif auth_method == 'sso':
        auth = awsauth(
            sso_url=sso_url,
            sso_role_name=sso_role_name,
            sso_account_id=sso_account_id
        )
        session = auth.sso()
    else:
        raise ValueError('auth_method is not defined.')
    return session


def crawler(session) -> list:
    """Create AWS account list."""
    if accounts_list_src == 'accounts':
        account_ids = aws_crawler.create_account_list(
            accounts
        )
    elif accounts_list_src == 'ou':
        account_ids = aws_crawler.list_ou_accounts(
            session,
            ou
        )
    elif accounts_list_src == 'statuses':
        account_ids = aws_crawler.list_accounts(
            session,
            statuses
        )
    else:
        raise ValueError('accounts_list_src is not defined.')
    return account_ids


def main():
    """Execute main function."""
    pass


if __name__ == '__main__':
    main()
