import aws_cdk as core
import aws_cdk.assertions as assertions

from kinesis_snowflake_pipeline.kinesis_snowflake_pipeline_stack import KinesisSnowflakePipelineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in kinesis_snowflake_pipeline/kinesis_snowflake_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = KinesisSnowflakePipelineStack(app, "kinesis-snowflake-pipeline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
