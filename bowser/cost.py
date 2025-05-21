import pulumi_aws as aws
import pulumi

config = pulumi.Config()
account_email = config.require_secret("account-email")
pagerduty_email = config.require_secret("pagerduty-email")

aws.budgets.Budget(
    "personal-infra-total-budget",
    budget_type="COST",
    limit_amount="40",
    limit_unit="USD",
    time_unit="MONTHLY",
    notifications=[
        {
            "comparison_operator": "GREATER_THAN",
            "threshold": 100,
            "threshold_type": "PERCENTAGE",
            "notification_type": "FORECASTED",
            "subscriber_email_addresses": [account_email, pagerduty_email],
        },
        {
            "comparison_operator": "GREATER_THAN",
            "threshold": 150,
            "threshold_type": "PERCENTAGE",
            "notification_type": "FORECASTED",
            "subscriber_email_addresses": [account_email, pagerduty_email],
        },
        {
            "comparison_operator": "GREATER_THAN",
            "threshold": 85,
            "threshold_type": "PERCENTAGE",
            "notification_type": "FORECASTED",
            "subscriber_email_addresses": [account_email],
        },
        {
            "comparison_operator": "GREATER_THAN",
            "threshold": 50,
            "threshold_type": "PERCENTAGE",
            "notification_type": "ACTUAL",
            "subscriber_email_addresses": [account_email],
        },
        {
            "comparison_operator": "GREATER_THAN",
            "threshold": 90,
            "threshold_type": "PERCENTAGE",
            "notification_type": "ACTUAL",
            "subscriber_email_addresses": [account_email],
        },
    ],
)