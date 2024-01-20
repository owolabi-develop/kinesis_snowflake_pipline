import json
import boto3
import os
import random
from faker import Faker
import csv
from pprint import pprint



fake = Faker()

def generate_customer_order_data():
    
    """Generate a fake sales data."""
    
    products = ['iPhone', 'Samsung Galaxy', 'MacBook Pro', 'iPad', 'Apple Watch', 'Dell XPS', 'Sony TV', 'Nintendo Switch',
                'LG OLED TV', 'Amazon Echo', 'Google Pixel', 'Microsoft Surface', 'HP Spectre x360', 'Canon EOS', 
                'Bose QuietComfort', 'Fitbit Versa', 'GoPro Hero', 'Xbox Series X', 'PlayStation 5', 'Kindle Paperwhite',
                'Lenovo ThinkPad', 'Raspberry Pi', 'DJI Mavic', 'Garmin Forerunner', 'Beats Studio', 'JBL Flip',
                'Anker PowerCore', 'Logitech G502', 'Corsair K95', 'SteelSeries Arctis', 'Samsung SSD', 'Western Digital HDD',
                'Nikon DSLR', 'ASUS ROG', 'Alienware Area-51', 'Panasonic Lumix', 'Sony Alpha', 'Nintendo 3DS', 'Sony PlayStation VR',
                'Oculus Quest', 'Sega Genesis Mini', 'Atari VCS', 'Brother Laser Printer', 'Epson EcoTank', 'Dyson Air Purifier',
                'Philips Hue', 'Nest Thermostat', 'Ring Video Doorbell', 'Lutron Caseta', 'iRobot Roomba', 'Ecobee SmartThermostat',
                'Sennheiser HD', 'Roku Streaming Stick', 'Fire TV Stick', 'Chromecast', 'Apple TV', 'Samsung Soundbar',
                'Bowers & Wilkins Speakers', 'Sonos Beam', 'Marshall Bluetooth Speaker', 'Jabra Elite', 'Bose SoundLink',
                'UE Megaboom', 'Harman Kardon Go+Play', 'Skullcandy Crusher', 'HyperX Cloud', 'Audio-Technica ATH-M50x',
                'Sennheiser Momentum', 'AKG K240', 'Shure SE215', 'Beats Solo', 'Plantronics BackBeat', 'Rode VideoMic',
                'Blue Yeti', 'Zoom H4n', 'GoPro Hero Session', 'DJI Osmo', 'Polaroid Snap', 'Fujifilm Instax', 'Canon PowerShot',
                'Sony Cyber-shot', 'Nikon Coolpix', 'GoPro MAX', 'Insta360 One', 'Ricoh Theta', 'Garmin VIRB', 'Olympus Tough',
                'Sony Handycam', 'Canon Vixia', 'Panasonic HC-V770', 'DJI Ronin', 'Zhiyun Crane', 'Manfrotto Tripod']
   
   
    
   

    customer_order_data_details = {
        'product': random.choice(products),
        'customer_name': fake.name(),
        'customer_email': fake.email(),
        'phone_number': fake.phone_number(),
        'address': fake.address(),
        'city': fake.city(),
        'shipping_address': fake.address(),
        "order_date": fake.date_this_year().strftime('%Y-%m-%d'),
        'quantity': random.randint(1, 5),
        'price': round(random.uniform(100, 2000), 2),
        'country': fake.country(),
        'payment_method': fake.random_element(elements=('Credit Card', 'PayPal', 'Cash on Delivery')),
        'status': fake.random_element(elements=('Processing', 'Shipped', 'Delivered', 'Cancelled'))
    }
    return customer_order_data_details

def generate_customer_data(num_customer_data):
    """Generate multiple fake real sales data ."""
    customer_data = [generate_customer_order_data() for _ in range(num_customer_data)]
    with open('customers.csv', 'w',newline='',encoding='utf-8') as csvfile:
        fieldnames = ['product', 'customer_name', 'customer_email', 'phone_number', 'address', 'city','shipping_address', 'order_date', 'quantity', 'price', 'country', 'payment_method','status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',',doublequote=False)
        writer.writeheader()
        for customer in customer_data:
            writer.writerow(customer)
    pprint(customer_data,indent=2)
    return customer_data

def handler(event,context):
    
    kinesis_client = boto3.client('kinesis')
    
    cuatomer_orders_data = generate_customer_data(200)
    
    for customerdata in cuatomer_orders_data:
        response = kinesis_client.put_record(
            StreamName=os.environ['STREAM_NAME'],
            Data=json.dumps(customerdata).encode('utf-8'),
            PartitionKey=customerdata['product']
        )
    return response
    


generate_customer_data(100)