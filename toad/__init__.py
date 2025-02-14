import pulumi
import pulumi_aws as aws
import json

ACCOUNT_ID = aws.get_caller_identity().account_id


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
                            "Federated": f"arn:aws:iam::{aws.get_caller_identity().account_id}:oidc-provider/token.actions.githubusercontent.com"
                        },
                        "Action": "sts:AssumeRoleWithWebIdentity",
                        "Condition": {
                            "StringEquals": {
                                "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                                "token.actions.githubusercontent.com:sub": "repo:pacorain/toad:environment:Home",
                            }
                        },
                    }
                ],
            }
        ),
    )

    publish_policy = aws.iam.Policy(
        "toad-config-publisher-policy",
        tags={"project": "toad", "pulumi": "true"},
        policy=pulumi.Output.all(role_id=github_actions_role.id).apply(
            lambda args: json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": ["s3:PutObject", "s3:GetObject"],
                            "Resource": [
                                f"arn:aws:s3:::pacorain-toad-configs/*",
                            ],
                        },
                        {
                            "Effect": "Allow",
                            "Action": ["s3:ListBucket"],
                            "Resource": [f"arn:aws:s3:::pacorain-toad-configs"],
                        },
                        {
                            "Effect": "Allow",
                            "Action": ["sts:AssumeRoleWithWebIdentity"],
                            "Resource": [
                                f"arn:aws:iam::{ACCOUNT_ID}:role/{args['role_id']}",
                            ],
                        },
                    ],
                }
            )
        ),
    )

    aws.iam.RolePolicyAttachment(
        "toad-github-actions-policy-attachment",
        policy_arn=publish_policy.arn,
        role=github_actions_role.name,
    )

    aws.iam.OpenIdConnectProvider(
        "toad-github-actions-oidc-provider",
        url="https://token.actions.githubusercontent.com",
        client_id_lists=["sts.amazonaws.com"],
    )
