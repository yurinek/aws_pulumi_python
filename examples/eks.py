import pulumi
import pulumi_aws as aws
import pulumi_eks as eks

main_vpc = aws.ec2.Vpc("main", cidr_block="10.0.0.0/16")

main_subnet = aws.ec2.Subnet("main_subnet",
    vpc_id=main_vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    tags={
        "Name": "main_subnet",
    })

secondary_subnet = aws.ec2.Subnet("secondary_subnet",
    vpc_id=main_vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="us-east-1b",
    tags={
        "Name": "secondary_subnet",
    })  

eks_cluster = aws.eks.Cluster("eks_cluster",
    name="eks_cluster",
    # role arn with eks cluster permissions needs to exist in aws account (number is the aws account id)
    role_arn="arn:aws:iam::123456789011:role/eksClusterRole",
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        subnet_ids=[
            main_subnet.id,
            secondary_subnet.id,
        ],
    )
    )

# Get the necessary cluster's details.
cluster_endpoint = eks_cluster.endpoint
cluster_certificate_authority_data = eks_cluster.certificate_authority.data

# Fetch the AWS IAM user credentials.
user_credentials = aws.get_caller_identity()

# Construct the kubeconfig data.
kubeconfig_data = {
    "apiVersion": "v1",
    "kind": "Config",
    "clusters": [{
        "cluster": {
            "server": cluster_endpoint,
            "certificate-authority-data": cluster_certificate_authority_data,
        },
        "name": "kubernetes",
    }],
    "contexts": [{
        "context": {
            "cluster": "kubernetes",
            "user": "aws",
        },
        "name": "aws",
    }],
    "current-context": "aws",
    "users": [{
        "name": "aws",
        "user": {
            "exec": {
                "apiVersion": "client.authentication.k8s.io/v1alpha1",
                "command": "aws",
                "args": ["eks", "get-token", "--cluster-name", eks_cluster.name],
            },
        },
    }],
}

@pulumi.runtime.test
def test_user_credentials(args):
    assert expected_output == user_credentials

# Print the kubeconfig data.
pulumi.export('kubeconfig', kubeconfig_data)
pulumi.export("endpoint", eks_cluster.endpoint)
pulumi.export("kubeconfig-certificate-authority-data", eks_cluster.certificate_authority.data)
