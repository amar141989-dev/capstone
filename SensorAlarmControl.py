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
from boto3.dynamodb.conditions import Key, Attr



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



# Use existing table soilsensor_data to query and scan the data
soil_sensor_table = dynamodb.Table('soil_sensor_data')

# Use existing table soilsensor_data to query and scan the data
weather_table = dynamodb.Table('weather_data')

# Use existing table soil_sensor_alarm to write data, query and scan the data
soil_sensor_alarm_table = dynamodb.Table('soil_sensor_alarm')

# Use existing table sprinkler_switch to write data
sprinkler_switch_table = dynamodb.Table('sprinkler_switch')



minutes = ['2021-03-10 00:00', '2021-03-10 01:00', '2021-03-10 02:00', '2021-03-10 03:00', '2021-03-10 04:00',
           '2021-03-10 05:00', '2021-03-10 06:00', '2021-03-10 07:00', '2021-03-10 08:00', '2021-03-10 09:00',
           '2021-03-10 10:00', '2021-03-10 11:00', '2021-03-10 12:00', '2021-03-10 13:00', '2021-03-10 14:00',
           '2021-03-10 15:00', '2021-03-10 16:00', '2021-03-10 17:00', '2021-03-10 18:00', '2021-03-10 19:00',
           '2021-03-10 20:00', '2021-03-10 21:00', '2021-03-10 22:00', '2021-03-10 23:00']

devices = ['soil_sensor_1', 'soil_sensor_2', 'soil_sensor_3', 'soil_sensor_4', 'soil_sensor_5',
           'soil_sensor_6','soil_sensor_7','soil_sensor_8','soil_sensor_9','soil_sensor_10']

sprinklers = ['sprinkler_1', 'sprinkler_2']

#SensorAlarm1-10 are OFF
sensorAlarm = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


#Initialize all Alarm OFF
Alarm = 0
for d in range(10):
    soil_sensor_alarm_table.put_item(
        Item={'deviceid': devices[d], 'alarm': Alarm}
        )

#Initialize all Sprinklers OFF
Switch = 0
for s in range(2):
    sprinkler_switch_table.put_item(
        Item={'sprinklerid': sprinklers[s], 'switch': Switch}
        )

for m in range(24):
    for d in range(10):
        print("Minute %d CurrentTime = %s DeviceId = %s" %((m+1), minutes[m], devices[d]))
        #Scan soil_sensor_table for Minute1, DataType=Temperature, deviceid
        responseSoilTemperature = soil_sensor_table.scan(
            FilterExpression=Attr('timestamp').begins_with(minutes[m]) & Attr('datatype').eq('Temperature') & Attr('deviceid').eq(devices[d])
        )
        itemsSoilTemperature = responseSoilTemperature['Items']
        print(itemsSoilTemperature)
        #Calculate AvgSoilTemperature for Minute1
        AvgSoilTemperature = 0.0
        SoilTemperature = 0.0
        countSoilTemperature = 0
        loopcount1 = 0
        for i in itemsSoilTemperature:
            SoilTemperature = SoilTemperature + itemsSoilTemperature[loopcount1]["value"]
            countSoilTemperature = loopcount1
            loopcount1 = loopcount1 + 1
        AvgSoilTemperature = SoilTemperature/(countSoilTemperature + 1)
        AvgSoilTemperature = round(AvgSoilTemperature, 1)
        print("AvgSoilTemperature = %f" % (AvgSoilTemperature))

        #Scan weather_table for Minute1, DataType=Temperature
        responseTemperature = weather_table.scan(
            FilterExpression=Attr('timestamp').begins_with(minutes[m]) & Attr('datatype').eq('Temperature')
        )
        itemsTemperature = responseTemperature['Items']
        print(itemsTemperature)
        #Calculate AvgTemperature for Minute1
        AvgTemperature = 0.0
        Temperature = 0.0
        countTemperature = 0
        loopcount2 = 0
        for i in itemsTemperature:
            Temperature = Temperature + itemsTemperature[loopcount2]["value"]
            countTemperature = loopcount2
            loopcount2 = loopcount2 + 1
        AvgTemperature = Temperature/(countTemperature + 1)
        AvgTemperature = round(AvgTemperature, 1)
        print("AvgTemperature = %f" % (AvgTemperature))

        #Calculate difference in Temperature
        if ((AvgTemperature - AvgSoilTemperature) > 2):
            Alarm = 1
        if ((AvgTemperature - AvgSoilTemperature) < 2):
            Alarm = 0

        #Update Sensor Alarm state to Table soil_sensor_alarm 
        soil_sensor_alarm_table.put_item(
            Item={'deviceid': devices[d], 'alarm': Alarm}
            )

    #Read Table soil_sensor_alarm.
    #If SensorAlarm1-5 are ON, Switch ON Sprinkler1. If SensorAlarm6-10 are ON, Switch ON Sprinkler2
    for d1 in range(10):
        responseAlarm = soil_sensor_alarm_table.scan(
            FilterExpression=Attr('deviceid').eq(devices[d1])
        )
        itemsAlarm = responseAlarm['Items']
        print(itemsAlarm)
        sensorAlarm[d1] = itemsAlarm[0]["alarm"]
        
    if ( sensorAlarm[0] == 1 and sensorAlarm[1] == 1 and sensorAlarm[2] == 1 and sensorAlarm[3] == 1 and sensorAlarm[4] == 1):
        #Switch ON Sprinkler1
        #Update Sprinkler Switch to Table sprinkler_switch 
        sprinkler_switch_table.put_item(
            Item={'sprinklerid': sprinklers[0], 'switch': 1}
            )
        
    if ( sensorAlarm[5] == 1 and sensorAlarm[6] == 1 and sensorAlarm[7] == 1 and sensorAlarm[8] == 1 and sensorAlarm[9] == 1):
        #Switch ON Sprinkler2
        #Update Sprinkler Switch to Table sprinkler_switch 
        sprinkler_switch_table.put_item(
            Item={'sprinklerid': sprinklers[1], 'switch': 1}
            )
        
    if ( sensorAlarm[0] == 0 or sensorAlarm[1] == 0 or sensorAlarm[2] == 0 or sensorAlarm[3] == 0 or sensorAlarm[4] == 0):
        #Switch OFF Sprinkler1
        #Update Sprinkler Switch to Table sprinkler_switch 
        sprinkler_switch_table.put_item(
            Item={'sprinklerid': sprinklers[0], 'switch': 0}
            )
        
    if ( sensorAlarm[5] == 0 or sensorAlarm[6] == 0 or sensorAlarm[7] == 0 or sensorAlarm[8] == 0 or sensorAlarm[9] == 0):
        #Switch OFF Sprinkler2
        #Update Sprinkler Switch to Table sprinkler_switch 
        sprinkler_switch_table.put_item(
            Item={'sprinklerid': sprinklers[1], 'switch': 0}
            )
































        
        
    









