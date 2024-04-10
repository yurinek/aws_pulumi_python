"""An AWS Python Pulumi program for ec2"""

import pulumi
import pulumi_aws as aws

# Read the stack configuration and its variables (if namespace not set, it defaults to project name)
config = pulumi.Config()
# Read the stack configuration from aws namespace
config_aws = pulumi.Config('aws')
region = config_aws.require('region')
ami = config.require('ami')
customer_name = config.require('customer')
stage = pulumi.get_stack()


main_vpc = aws.ec2.Vpc(f"{customer_name}-{stage}-vpc",
    cidr_block="172.16.0.0/16",
    tags={
        "Name": f"{customer_name}-{stage}-vpc",
    })
main_subnet = aws.ec2.Subnet(f"{customer_name}-{stage}-subnet",
    vpc_id=main_vpc.id,
    cidr_block="172.16.10.0/24",
    availability_zone="us-east-1a",
    tags={
        "Name": f"{customer_name}-{stage}-subnet",
    })
network_adapter = aws.ec2.NetworkInterface(f"{customer_name}-{stage}-na",
    subnet_id=main_subnet.id,
    private_ips=["172.16.10.100"],
    tags={
        "Name": f"{customer_name}-{stage}-na",
    })
vm = aws.ec2.Instance(f"{customer_name}-{stage}-vm",
    #You can find AMI IDs in AWS Management Console under EC2 service by navigating to "AMIs" in "Images" section. Make sure youre looking at the correct region
    ami=ami,
    instance_type=aws.ec2.InstanceType.T2_MICRO,
    tags={
        "Name": f"{customer_name}-{stage}-vm",
    },
    network_interfaces=[aws.ec2.InstanceNetworkInterfaceArgs(
        network_interface_id=network_adapter.id,
        device_index=0,
    )]
    )
