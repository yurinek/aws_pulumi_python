"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket) with bucket parameter for custom names
bucket = s3.Bucket('main-bucket', bucket='my-bucket-name-without-random-suffix')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
