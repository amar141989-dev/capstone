from AwsCloudHelper import AwsCloudHelper
from datetime import timedelta
from datetime import datetime
from datetime import time
from datetime import timezone

from os.path import abspath
from Simulator.Client.AWSClient import AWSClient
from botocore.exceptions import ClientError


import schedule
import json
import random
import boto3

from boto3 import Session
from botocore.config import Config
import constants

class CreateDynamoTables:
    def __init__(self):
        
        self.weather_dataTableName=constants.weather_dataTableName
        self.soil_sensor_alarmTableName=constants.soil_sensor_alarmTableName
        self.soil_sensor_data_alarmTableName=constants.soil_sensor_data_alarmTableName
        self.sprinkler_switch_alarmTableName=constants.sprinkler_switch_alarmTableName

        # Create a low-level client with the service name
        self.dynamodb = boto3.resource('dynamodb')

    def createWeatherTable(self):

        try:

            # Creat table weather_data
            weather_table = self.dynamodb.create_table(
                TableName=self.weather_dataTableName,
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
            weather_table.meta.client.get_waiter('table_exists').wait(TableName=self.weather_dataTableName)

            print("Table with name {0} created in DynamoDB ".format(self.weather_dataTableName))
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("Dynamo table  {0} already exists".format(self.weather_dataTableName))
            else:
                print("Unexpected error: %s" % e)

    def createSoilSensorAlarmTable(self):
        
        try:

            # Creat table soil_sensor_alarm
            soil_sensor_alarm_table = self.dynamodb.create_table(
            TableName=self.soil_sensor_alarmTableName,
            AttributeDefinitions=[
                {
                    'AttributeName': 'deviceid',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'alarmtimestamp',
                    'AttributeType': 'S'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'deviceid',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'alarmtimestamp',
                    'KeyType': 'RANGE'
                }     
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1000,
                'WriteCapacityUnits': 10000
            }
            )

            # Wait until the table exists.
            soil_sensor_alarm_table.meta.client.get_waiter('table_exists').wait(TableName=self.soil_sensor_alarmTableName)
            print("Table with name {0} created in DynamoDB ".format(self.soil_sensor_alarmTableName))

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("Dynamo table  {0} already exists".format(self.soil_sensor_alarmTableName))
            else:
                print("Unexpected error: %s" % e)

    def createSoilSensorDataTable(self):

        try:

            # Creat table soil_sensor_data
            soil_sensor_table = self.dynamodb.create_table(
            TableName=self.soil_sensor_data_alarmTableName,
            AttributeDefinitions=[
                {
                    'AttributeName': 'deviceId',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'devicetimestamp',
                    'AttributeType': 'S'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'deviceId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'devicetimestamp',
                    'KeyType': 'RANGE'
                }     
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1000,
                'WriteCapacityUnits': 10000
            }
            )

            # Wait until the table exists.
            soil_sensor_table.meta.client.get_waiter('table_exists').wait(TableName=self.soil_sensor_data_alarmTableName)
            print("Table with name {0} created in DynamoDB ".format(self.soil_sensor_data_alarmTableName))
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("Dynamo table  {0} already exists".format(self.soil_sensor_data_alarmTableName))
            else:
                print("Unexpected error: %s" % e)

    def createSprinklerSwitchTable(self):

        try:

            # Creat table sprinkler_switch
            sprinkler_switch_table = self.dynamodb.create_table(
            TableName=self.sprinkler_switch_alarmTableName,
            AttributeDefinitions=[
                {
                    'AttributeName': 'sprinklerid',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'switch',
                    'AttributeType': 'S'
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'sprinklerid',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'switch',
                    'KeyType': 'RANGE'
                }     
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1000,
                'WriteCapacityUnits': 10000
            }
            )

            # Wait until the table exists.
            sprinkler_switch_table.meta.client.get_waiter('table_exists').wait(TableName=self.sprinkler_switch_alarmTableName)
            print("Table with name {0} created in DynamoDB ".format(self.sprinkler_switch_alarmTableName))
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("Dynamo table  {0} already exists".format(self.sprinkler_switch_alarmTableName))
            else:
                print("Unexpected error: %s" % e)

    def deleteAllTables(self):
        


        try:

            devices_table = self.dynamodb.Table(self.soil_sensor_alarmTableName)
            devices_table.delete()
            print("Table '{0}' deleted ".format(self.soil_sensor_alarmTableName))
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("Can not delete Dynamo table  '{0}' as it does not exists".format(self.soil_sensor_alarmTableName))
            else:
                print("Unexpected error: %s" % e)

        try:

            devices_table = self.dynamodb.Table(self.soil_sensor_data_alarmTableName)
            devices_table.delete()
            print("Table '{0}' deleted ".format(self.soil_sensor_data_alarmTableName))
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("Can not delete Dynamo table  '{0}' as it does not exists".format(self.soil_sensor_data_alarmTableName))
            else:
                print("Unexpected error: %s" % e)

