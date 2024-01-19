from constructs import Construct
import aws_cdk as cdk
from  aws_cdk import (
    Stack,
    aws_s3 as _s3,
    RemovalPolicy


)





class S3bucketStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **Kwargs):
        super().__init__(scope, construct_id, **Kwargs)
        
        
          ## landing_zone_bucket
        
        landing_zone_bucket = _s3.Bucket(self, "landing_zone_bucket",
                    bucket_name="landing-zone-bucket",
                    removal_policy=RemovalPolicy.DESTROY
                )
        
        ## airflow dags bucket
        airflow_dags_bucket = _s3.Bucket(self, "ImportedBucket",
                    bucket_name="airflow-scripts-bucket",
                    removal_policy=RemovalPolicy.DESTROY,
                    versioned=True
                )
        
        
        
       
       

        
        
       