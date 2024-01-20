from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    Duration,
    aws_lambda_event_sources,
    aws_kinesis as kinesis,
    aws_s3 as _s3,

    
)
STREAM_ARN= "arn:aws:kinesis:us-east-1:851725420683:stream/salesData"

ENVIRONMENT = {
    "BUCKET_NAME":"landing-zone-customers-bucket"
}
class ConsumerStack(Stack):
     def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope,construct_id, **kwargs)
        
        lambda_consumer_role = iam.Role(
            self,
            id="lambdaRole",
             assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
             managed_policies=[
                 iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
             ]
        )
        
        
       
        
        
        
        lambda_customer_data_consumer = _lambda.Function(self,
                                             "customerDataconsumer",
                                             runtime=_lambda.Runtime.PYTHON_3_10,
                                             code=_lambda.Code.from_asset("lambda"),
                                             handler="sales_data_consumer.handler",
                                             timeout=Duration.seconds(60),
                                             role=lambda_consumer_role,
                                             environment=ENVIRONMENT,
                                             )
        
       
        destination_bucket = _s3.Bucket.from_bucket_attributes(self, "destination_bucketImported",
                    bucket_arn="arn:aws:s3:::landing-zone-customers-bucket"
                )
        
        
        destination_bucket.grant_read_write(lambda_customer_data_consumer)
        
        stream = kinesis.Stream.from_stream_arn(self,
                                                "sales_data",
                                                stream_arn=STREAM_ARN)
        
        lambda_customer_data_consumer.add_event_source(
            aws_lambda_event_sources.KinesisEventSource(
                stream=stream,
                batch_size=100,
                starting_position=_lambda.StartingPosition.LATEST
                
            )
        )
        
        
        
        
        
        
        