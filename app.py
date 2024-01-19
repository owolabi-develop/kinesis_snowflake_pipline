#!/usr/bin/env python3
import os

import aws_cdk as cdk
from firehoseStack.kinesis_firehose_stack import KinesisFireHoseStack
from S3bucketStack.s3bucket_stacks import S3bucketStack
from lambdaStack.lambda_producer_stack import SalesDataStack





env_US = cdk.Environment(account="851725420683",region='us-east-1')
app = cdk.App()

SalesDataStack(app,"SalesDataStack",env=env_US)

KinesisFireHoseStack(app,"KinesisFireHoseStack",env=env_US)

S3bucketStack(app,"S3bucketStac",env=env_US)





cdk.Tags.of(app).add("ProjectOwner","Owolabi akintan")
cdk.Tags.of(app).add("ProjectName","kinesis-snowflake-pipline")

app.synth()
