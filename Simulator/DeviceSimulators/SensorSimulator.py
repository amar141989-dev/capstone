from datetime import timedelta
from datetime import datetime
from datetime import timezone
import os

from os.path import abspath
from OpenWeatherMap import OpenWeatherMap
from Simulator.Client.AWSClient import AWSClient

import schedule
import time
import json
import random
import pathlib
from AwsCloudHelper import AwsCloudHelper
from botocore.exceptions import ClientError

import constants

class SensorSimulator:

    def __init__(self):
        self.ach=AwsCloudHelper("")
        self.allSensorsWithCert=[]
        pass

    def __getsensors(self):
        if len(self.allSensorsWithCert)==0:
            allSensors =self.ach.get_thing_list("","Sensor")
            for sensor in allSensors:
                sensorWIthCA = self.ach.get_farm_tags_by_thing(sensor["thingName"])
                self.allSensorsWithCert.append(sensorWIthCA)

        print("Avaialble sensor count is {0}", len(self.allSensorsWithCert))


    def __get_next_time(self, interval_minutes):
        future_trigger_time = datetime.now() + timedelta(minutes=interval_minutes)
        return future_trigger_time
    
    def __startsensors(self):
        #get sensors
        self.__getsensors()
        OWP = OpenWeatherMap(constants.weather_api_key)
        next_trigger = self.__get_next_time(-1)
        humidity, temperature = (0,0)
        
        absPath = os.path.abspath(constants.absolute_certificate_path)
        for sensor in self.allSensorsWithCert:
            try:
                message = {}
                host=sensor['host']
                rootCAPath=os.path.join(absPath, sensor['rootCAPath'])
                certificatePath=os.path.join(absPath, sensor['certificatePath'])
                privateKeyPath=os.path.join(absPath, sensor['privateKeyPath'])
                port=sensor['port']
                clientId=sensor['clientId']
                topic=sensor['topic']
                client = AWSClient(host, rootCAPath, certificatePath, privateKeyPath, port, clientId, topic)
                message['deviceId'] = sensor['deviceId']
                message['lat'] = sensor['lat']
                message['lng'] = sensor['lng']
                message['devicetimestamp']=str(datetime.now(timezone.utc))

                #Get new temp and humidty data in every 15 minutes
                #otherwise fail for rate limiting 
                if next_trigger<datetime.now():
                    humidity,temperature = OWP.get_humidity_temp(float(message['lat']), float(message['lng']))
                    next_trigger = self.__get_next_time(15)

                message['humidity'] = humidity
                message['moisture'] = float(random.normalvariate(99, 1.5))
                message['temperature'] = temperature
                message['sprinkler'] = sensor['sprinkler']
                message['farm'] = sensor['Farm']
                messageJson = json.dumps(message)
                client.topic
                client.publish(messageJson,1)
                print('Published topic %s: %s\n' % (client.topic, message))

            except ClientError as e:
                print("Publsh failed Message {0}".format(message))
                print("Unexpected error: %s" % e)

    def startSimulation(self):
        schedule.every(4).seconds.do(self.__startsensors)
        while 1:
            schedule.run_pending()
            time.sleep(5)


    
            
