from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException
from AWSIoTPythonSDK.core.protocol.internal.defaults import DEFAULT_OPERATION_TIMEOUT_SEC
import logging
import datetime
import argparse
import json
import random
import csv
import time
import sched

import boto3
from botocore.config import Config

ACCESS_KEY = 'type here access key'
SECRET_KEY = 'type here secret access key'

my_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# Create a low-level client with the service name
dynamodb = boto3.client('dynamodb', config=my_config, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Creat table soil_sensor_data
soil_sensor_table = dynamodb.create_table(
    TableName='soil_sensor_data',
    AttributeDefinitions=[
        {
            'AttributeName': 'deviceid',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'timestamp',
            'AttributeType': 'S'
        }
    ],
    KeySchema=[
        {
            'AttributeName': 'deviceid',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'timestamp',
            'KeyType': 'RANGE'
        }     
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1000,
        'WriteCapacityUnits': 10000
    }
)

# Wait until the table exists.
soil_sensor_table.meta.client.get_waiter('table_exists').wait(TableName='soil_sensor_data')
