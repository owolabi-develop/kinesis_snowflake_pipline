import csv
import json
import boto3
import base64
import os

def handler(event, context):
    BUCKET_NAME = os.environ['BUCKET_NAME']
    s3_client = boto3.client('s3')
    for i, record in enumerate(event['Records']):
        record_data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(record_data)

        # Assuming data is a dictionary where each key represents a column in the CSV
        csv_filename = "/tmp/customer.csv"  # Create a unique filename for each record
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=data.keys())
            csv_writer.writeheader()
            csv_writer.writerow(data)  # Write the data to the CSV file

        # Upload the CSV file to S3
    s3_client.upload_file(csv_filename, BUCKET_NAME, 'customer.csv')

      
