"""An AWS Python Pulumi program for s3"""

import pulumi
from pulumi_aws import s3

# Read the stack configuration and its variables (if namespace not set, it defaults to project name)
config = pulumi.Config()
# Read the stack configuration from aws namespace
config_aws = pulumi.Config('aws')
region = config_aws.require('region')
customer_name = config.require('customer')
stage = pulumi.get_stack()

# Create S3 Bucket and format its name (random string is appended automatically)
bucket = s3.Bucket(f"{customer_name}-{stage}")

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)