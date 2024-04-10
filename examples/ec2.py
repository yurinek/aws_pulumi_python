import pulumi
import pulumi_aws as aws

main_vpc = aws.ec2.Vpc("main_vpc",
    cidr_block="172.16.0.0/16",
    tags={
        "Name": "main_vpc",
    })
main_subnet = aws.ec2.Subnet("main_subnet",
    vpc_id=main_vpc.id,
    cidr_block="172.16.10.0/24",
    availability_zone="us-east-1a",
    tags={
        "Name": "main_subnet",
    })
network_adapter = aws.ec2.NetworkInterface("main_network_interface",
    subnet_id=main_subnet.id,
    private_ips=["172.16.10.100"],
    tags={
        "Name": "main_network_interface",
    })
vm = aws.ec2.Instance("vm",
    #You can find AMI IDs in AWS Management Console under EC2 service by navigating to "AMIs" in "Images" section. Make sure youre looking at the correct region
    ami="ami-080e1f13689e07408",
    instance_type=aws.ec2.InstanceType.T2_MICRO,
    tags={
        "Name": "vm",
    },
    network_interfaces=[aws.ec2.InstanceNetworkInterfaceArgs(
        network_interface_id=network_adapter.id,
        device_index=0,
    )]
    )
