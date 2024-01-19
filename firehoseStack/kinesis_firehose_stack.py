from constructs import Construct
import aws_cdk as cdk
from  aws_cdk import (
    Stack,
    aws_kinesisfirehose as _firehose,
    aws_iam as _iam,
    aws_s3 as _s3,
    aws_s3_deployment as _s3deploy,

)


STREAM_ARN = "arn:aws:kinesis:us-east-1:851725420683:stream/salesData"


class KinesisFireHoseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **Kwargs):
        super().__init__(scope, construct_id, **Kwargs)
        
        firehose_role = _iam.Role(self,
                             "firshoserole",
                             assumed_by=_iam.ServicePrincipal('firehose.amazonaws.com'),
                             managed_policies=[
                                _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                                _iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                                _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                                #_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRedshiftFullAccess"),
                                _iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
                             ]
                             
                             )
        
        ##   destination_bucket
        
        destination_bucket = _s3.Bucket.from_bucket_attributes(self, "ImportedBucket",
                    bucket_arn="arn:aws:s3:::landing-zone-bucket"
                )
        
        ## airflow dags bucket arn
        airflow_dags_bucket = _s3.Bucket.from_bucket_attributes(self, "ImportedBucket",
                    bucket_arn="arn:aws:s3:::airflow-scripts-bucket"
                )
        

        
        ## kinesis firehose delivery stream
        firehose_delivery = _firehose.CfnDeliveryStream(self,id="firehose_delivery",
            
            ## kinesis connection
            kinesis_stream_source_configuration= _firehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty(
                kinesis_stream_arn= STREAM_ARN,
                role_arn=firehose_role.role_arn
            ),
            s3_destination_configuration=_firehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
                bucket_arn=destination_bucket.bucket_arn,
                role_arn=firehose_role.role_arn,    
            ),
            
            delivery_stream_name="sales-data",
            delivery_stream_type="KinesisStreamAsSource",  
        )
        
       
       
        
        
        ### deploy the arflow dags script 
        
        _s3deploy.BucketDeployment(self,"deployment",
                                  sources=[_s3deploy.Source.asset('dags/')],
                                  destination_bucket=airflow_dags_bucket.bucket_arn)
        
        
        
       