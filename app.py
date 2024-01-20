#!/usr/bin/env python3
import os

import aws_cdk as cdk

from S3bucketStack.s3bucket_stacks import S3bucketStack
from lambdaStack.lambda_producer_stack import LambdaSalesDataStack
from lambdaStack.data_consumer_stack import ConsumerStack
from kinesisStack.kinesis_stack import KinesisStreamStack





env_US = cdk.Environment(account="851725420683",region='us-east-1')
app = cdk.App()
KinesisStreamStack(app,"KinesisStreamStack",env=env_US)
LambdaSalesDataStack(app,"LambdaSalesDataStack",env=env_US)

ConsumerStack(app,"ConsumerStack",env=env_US)


S3bucketStack(app,"S3bucketStack",env=env_US)







cdk.Tags.of(app).add("ProjectOwner","Owolabi akintan")
cdk.Tags.of(app).add("ProjectName","kinesis-snowflake-pipline")

app.synth()
