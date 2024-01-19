from constructs import Construct
import aws_cdk as cdk
from  aws_cdk import (
    Stack,
    Duration,
    aws_iam as _iam,
    aws_lambda as _lambda,
)

ENVIRONMENT = {
    "STREAM_NAME":"salesData"
}


class SalesDataStack(Stack):
     def __init__(self, scope: Construct, construct_id: str, **Kwargs):
        super().__init__(scope, construct_id, **Kwargs)
        
        lambda_role = _iam.Role(
            self,
            "lambdaRole",
             assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
             managed_policies=[
                 _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                 _iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                 _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                
             ]
        )
        
        sales_data_layer = _lambda.LayerVersion(
            self,
            "salesdatalayer",
            code=_lambda.AssetCode("layer/sale_layer")
        )
        
        
        
        lambda_sales_data_producer = _lambda.Function(self,
                                             "propertiesdataproducer",
                                             runtime=_lambda.Runtime.PYTHON_3_12,
                                             code=_lambda.Code.from_asset("lambda"),
                                             handler="sales_data_producer.handler",
                                             timeout=Duration.minutes(3),
                                             layers=[sales_data_layer],
                                             role=lambda_role,
                                             environment=ENVIRONMENT
                                             )
        
     