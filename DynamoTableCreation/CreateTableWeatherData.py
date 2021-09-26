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
from boto3 import Session

def createWeatherTable(self):
    ACCESS_KEY = 'type here access key'
    SECRET_KEY = 'type here secret access key'

    session = Session()
    credentials = session.get_credentials()
    # Credentials are refreshable, so accessing your access key / secret key
    # separately can lead to a race condition. Use this to get an actual matched
    # set.
    current_credentials = credentials.get_frozen_credentials()

    # I would not recommend actually printing these. Generally unsafe.
    print(current_credentials.access_key)
    print(current_credentials.secret_key)
    # print(current_credentials.token)

    ACCESS_KEY =current_credentials.access_key
    SECRET_KEY = current_credentials.secret_key

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

    # Creat table weather_data
    weather_table = dynamodb.create_table(
        TableName='weather_data',
        AttributeDefinitions=[
            {
                'AttributeName': 'latitude',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'longitude',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'latitude',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'longitude',
                'KeyType': 'RANGE'
            }     
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1000,
            'WriteCapacityUnits': 10000
        }
    )

    # Wait until the table exists.
    weather_table.meta.client.get_waiter('table_exists').wait(TableName='weather_data')
