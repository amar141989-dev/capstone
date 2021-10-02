import sys
import boto3
import datetime
from datetime import timezone
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

class Database:

    def __init__(self, dynamodb=None, dynamodb_client=None):
        
        self.date_format="%Y-%m-%dT%H:%M:%SZ"

        if not dynamodb:
            self.dynamodb = boto3.resource('dynamodb')
            self.dynamodb_client = boto3.client('dynamodb')
        else:
            self.dynamodb=dynamodb
            self.dynamodb_client = dynamodb_client

    #Create table into dynamo db 
    def create_table(self, tableName, keys, attributes):
        try:
            table = self.dynamodb.create_table(
                TableName=tableName,
                KeySchema=keys,
                AttributeDefinitions=attributes,
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            return table
        except:
            print("Error in get_data_by_date_range():", sys.exc_info()[0])

        return None

    #Insert/update item into dynamo table 
    def insert_data(self, tableName, data_item):
        try:
            table=self.dynamodb.Table(tableName)
        
            response = table.put_item(
            Item=data_item
            )
            return response
        except:
            print("Error in insert_data():", sys.exc_info()[0])    
        
        return None

    def get_data(self, tableName, max_record):

        try:
            resp = self.dynamodb_client.scan(
                    TableName=tableName,
                    Limit=max_record)
                        
            return resp['Items']
        except ClientError as e:
            print(e.response['Error']['Message'])
    
    def get_data_by_key(self, tableName, key_value):

        try:
            resp = self.dynamodb_client.query(
                    TableName=tableName,
                    KeyConditionExpression='deviceid = :deviceid',
                     ExpressionAttributeValues={
                        ':deviceid': {'S': key_value}
                     })
            
            return resp['Items']
        except ClientError as e:
            print(e.response['Error']['Message'])
            
    
    def get_data_since_by_key(self, tableName, key_value, sinceLastNMinutes):

        try:
            
            time_change = datetime.timedelta(minutes=sinceLastNMinutes)
            timerInterval = str(datetime.datetime.now(timezone.utc) - time_change)

            resp=self.dynamodb_client.query(
                    TableName=tableName,
                    KeyConditionExpression='deviceId = :deviceid and devicetimestamp > :deviceTs',
                     ExpressionAttributeValues={
                        ':deviceid': {'S': key_value},
                        ':deviceTs': {'S': timerInterval}
                     })
            
            return resp["Items"] 

        except ClientError as e:
            print(e.response['Error']['Message'])