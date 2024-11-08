# AWS SSO Migration Steps

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
- Execute aws_sso_get.
- Execute aws_sso_mappings.
- Manually replace remaining old identities if necessary.
- Ensure output details are correct and perform manual fixes if necessary.

## During SSO Migration

- Switch IdP.
- Execute aws_sso_json.
- Execute aws_sso_assign.
