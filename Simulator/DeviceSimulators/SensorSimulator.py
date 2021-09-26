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

import constants

class SensorSimulator:

    def __init__(self):
        self.ach=AwsCloudHelper("")
        self.allSensorsWithCert=[]
        # self.clients={}
        self.farmWeather={}
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
        print('BEGIN __startsensors')

        #get sensors
        self.__getsensors()
        OWP = OpenWeatherMap(constants.weather_api_key)
        next_trigger = self.__get_next_time(-1)
        humidity, temperature = (0,0)
        absPath = os.path.abspath(constants.absolute_certificate_path)
        
        
        for sensor in self.allSensorsWithCert:
            print('Forming data for {0}'.format(sensor['deviceId']))
            message = {}
            host=sensor['host']
            rootCAPath=os.path.join(constants.absolute_certificate_path, sensor['rootCAPath'])
            certificatePath=os.path.join(constants.absolute_certificate_path, sensor['certificatePath'])
            privateKeyPath=os.path.join(constants.absolute_certificate_path, sensor['privateKeyPath'])
            port=sensor['port']
            clientId=sensor['clientId']
            topic=sensor['topic']
            
            client = AWSClient(host, rootCAPath, certificatePath, privateKeyPath, port, clientId, topic)

            message['deviceId'] = sensor['deviceId']
            message['lat'] = sensor['lat']
            message['lng'] = sensor['lng']
            message['devicetimestamp']=str(datetime.now(timezone.utc))

            next_trigger, humidity, temperature = (self.__get_next_time(-1), 0,0)
            if not sensor['Farm'] in self.farmWeather:
                humidity,temperature = OWP.get_humidity_temp(float(message['lat']), float(message['lng']))
                next_trigger = self.__get_next_time(15)
                self.farmWeather[sensor['Farm']]=(next_trigger,humidity,temperature)
            else:
                next_trigger, humidity, temperature=self.farmWeather[sensor['Farm']]

            #Get new temp and humidty data in every 15 minutes
            #otherwise fail for rate limiting 
            if next_trigger<datetime.now():
                humidity,temperature = OWP.get_humidity_temp(float(message['lat']), float(message['lng']))
                next_trigger = self.__get_next_time(15)
                self.farmWeather[sensor['Farm']]=(next_trigger,humidity,temperature)

            message['humidity'] = humidity
            message['moisture'] = float(random.normalvariate(99, 1.5))
            message['temperature'] = temperature
            message['sprinkler'] = sensor['sprinkler']
            message['farm'] = sensor['Farm']
            messageJson = json.dumps(message)
            client.publish(messageJson,1)
            print('Published topic %s: %s\n' % (client.topic, message))
            client.disconnectClient()
            time.sleep(10)

        print('END __startsensors')
        

    def startSimulation(self):
        self.__startsensors()
        schedule.every(300).seconds.do(self.__startsensors)
        while 1:
            schedule.run_pending()
            time.sleep(5)


    
            
