import pulumi
import pulumi_aws as aws
import json


def run():
    bucket = aws.s3.BucketV2(
        "toad-configs",
        bucket="pacorain-toad-configs",
        tags={"project": "toad", "pulumi": "true"},
    )

    aws.s3.BucketLifecycleConfigurationV2(
        "toad-configs-lifecycle",
        bucket=bucket.id,
        rules=[
            aws.s3.BucketLifecycleConfigurationV2RuleArgs(
                id="toad-configs-lifecycle-rule",
                expiration=aws.s3.BucketLifecycleConfigurationV2RuleExpirationArgs(
                    days=90
                ),
                status="Enabled",
            )
        ],
    )

    publish_policy = aws.iam.Policy(
        "toad-config-publisher-policy",
        tags={"project": "toad", "pulumi": "true"},
        policy=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "s3:PutObject",
                        "Resource": "arn:aws:s3:::pacorain-toad-configs/*",
                    },
                    {
                        "Effect": "Allow",
                        "Action": "s3:ListBucket",
                        "Resource": "arn:aws:s3:::pacorain-toad-configs",
                    },
                    {
                        "Effect": "Allow",
                        "Action": "s3:GetObject",
                        "Resource": "arn:aws:s3:::pacorain-toad-configs/*",
                    },
                ],
            }
        ),
    )

    github_actions_role = aws.iam.Role(
        "toad-github-actions-role",
        tags={"project": "toad", "pulumi": "true"},
        assume_role_policy=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Federated": f"arn:aws:iam::{aws.get_caller_identity().account_id}:oidc-provider/tokens.actions.githubusercontent.com"
                        },
                        "Action": "sts:AssumeRoleWithWebIdentity",
                        "Condition": {
                            "StringEquals": {
                                f"token.actions.githubusercontet.com:sub": "repo:pacorain/toad:ref:refs/heads/main"
                            }
                        },
                    }
                ],
            }
        )
    )

    aws.iam.RolePolicyAttachment(
        "toad-github-actions-policy-attachment",
        policy_arn=publish_policy.arn,
        role=github_actions_role.name,
    )

    
