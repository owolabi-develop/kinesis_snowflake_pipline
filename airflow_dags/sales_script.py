from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator
from airflow.utils.dates import days_ago

from airflow.decorators import dag 
import datetime

SNOWFLAKE_CONN_ID = 'snowflake_con'

@dag(
    dag_id="customer_data_process",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def customer_data_process():
    
    S3_BUCKET_NAME = "landing-zone-customers-bucket"
    S3_FILE_PATH = f"s3://{S3_BUCKET_NAME}/customer.csv"
    SNOWFLAKE_STAGE ="raw_customer_stage"
    SNOWFLAKE_SAMPLE_TABLE ="CUSTOMER_TABLE"
    
    copy_into_table = CopyFromExternalStageToSnowflakeOperator(
        task_id="copy_into_Acustomer_table",
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        files=[S3_FILE_PATH],
        table=SNOWFLAKE_SAMPLE_TABLE,
        stage=SNOWFLAKE_STAGE,
        file_format="(type = 'CSV',field_delimiter = ',')",
        pattern=".*[.]csv",
    )
    copy_into_table
    

    


dag = customer_data_process()