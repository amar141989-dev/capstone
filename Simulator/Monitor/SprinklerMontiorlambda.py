import json
import boto3
from datetime import timezone
import datetime

def lambda_handler(event, context):
    
    iotclient = boto3.client('iot-data', region_name='us-east-1')
    
    dynamodbclient = boto3.client('dynamodb')
    paginator = dynamodbclient.get_paginator('scan')
    
    time_change = datetime.timedelta(minutes=100)
    timerInterval = str(datetime.datetime.now(timezone.utc) - time_change)
    
    operation_parameters = {
        'TableName': 'soil_sensor_data',
        'FilterExpression': 'humidity > :hum AND moisture > :moi AND temperature > :tem AND devicetimestamp > :deviceTs',
         'ExpressionAttributeValues': {
            ':hum': {'N': '50'},
            ':moi': {'N': '95'},
            ':tem': {'N': '20'},
            ':deviceTs': {'S': timerInterval}
          }
    }
    
    sprinklers=[]
    
    for page in paginator.paginate(**operation_parameters):
        for item in page['Items']:
            sprinklerName =item['sprinkler']['S']
            if (sprinklerName not in sprinklers):
                print ("Element Exists")
                print(item)
                sprinklers.append(sprinklerName)
            
    for sprinkler in set(sprinklers):
        response = iotclient.publish(topic='sprinkler/'+sprinkler,qos=1,payload=json.dumps({"Message":"Turn On"}))   
        print(sprinkler)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(sprinklers)
    }
