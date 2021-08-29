import sys
import boto3
import datetime
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

class Database:

    def __init__(self, dynamodb=None):
        
        self.date_format="%Y-%m-%dT%H:%M:%SZ"

        if not dynamodb:
            self.dynamodb = boto3.resource('dynamodb')
        else:
            self.dynamodb=dynamodb

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
