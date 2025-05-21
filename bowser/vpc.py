import pulumi_aws as aws

vpc = aws.ec2.Vpc(
    "bowser-vpc",
    cidr_block="10.11.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Project": "bowser",
    }
)

services_public_subnet = aws.ec2.Subnet(
    "services-public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.11.0.0/20",
    map_public_ip_on_launch=True,
    tags={
        "Project": "bowser",
    }
)

services_private_subnet = aws.ec2.Subnet(
    "services-private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.11.16.0/20",
    map_public_ip_on_launch=False,
    tags={
        "Project": "bowser",
    }
)




