# AWS SSO Migration Steps - Simplified

## Prerequisites

- SSO access with administrator privileges into the master account.
- Python >= 3.8.0.
- Python modules:
    - aws_crawler
    - multithreader
    - aws_authenticator
    - aws_administrator
    - boto3

## Before SSO Migration

- Get the list of migrated User and Group identities.
- Recreate all necessary Groups in the new AD with the correct memberships.
- Execute aws_sso_get for backup purposes.

## During SSO Migration

- Execute aws_sso_update.
- Switch IdP.
