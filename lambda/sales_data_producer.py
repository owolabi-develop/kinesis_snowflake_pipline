import json
import boto3
import os
import random
from faker import Faker
from decimal import Decimal


fake = Faker()

def generate_property():
   
    """Generate a fake sales data."""
    
   

    property_details = {  }
    return property_details

def generate_properties(num_properties):
    """Generate multiple fake real sales data ."""
    properties = [generate_property() for _ in range(num_properties)]
    return properties

def handler(event,context):
    
    kinesis_client = boto3.client('kinesis')
    
    properties_data = generate_properties(200)
    
    for properties in properties_data:
        response = kinesis_client.put_record(
            StreamName=os.environ['STREAM_NAME'],
            Data=json.dumps(properties).encode('utf-8'),
            PartitionKey=properties['']
        )
    return response
    
    
    