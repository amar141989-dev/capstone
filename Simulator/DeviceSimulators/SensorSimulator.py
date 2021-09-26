from datetime import timedelta
from datetime import datetime
from datetime import time
from datetime import timezone

from os.path import abspath
from OpenWeatherMap import OpenWeatherMap
from Simulator.Client.AWSClient import AWSClient

import schedule
import json
import random
from AwsCloudHelper import AwsCloudHelper

import constants

class SensorSimulator:

    def __init__(self):
        self.ach=AwsCloudHelper("")

        pass

    def __getsensors(self):
        allSensors =self.ach.get_thing_list("","Sensor")
        allSensorsWithCert=[]
        for sensor in allSensors:
            sensorWIthCA = self.ach.get_farm_tags_by_thing(sensor["thingName"])
            allSensorsWithCert.append(sensorWIthCA)

        print("Avaialble sensor count is {0}", len(allSensorsWithCert))
        return  allSensorsWithCert

    def __get_next_time(self, interval_minutes):
        future_trigger_time = datetime.now() + timedelta(minutes=interval_minutes)
        return future_trigger_time
    
    def __startsensors(self):
        #get sensors
        sensors = self.__getsensors()
        OWP = OpenWeatherMap(constants.weather_api_key)
        next_trigger = self.__get_next_time(-1)
        humidity, temperature = (0,0)
        while True:
            for sensor in sensors:
                message = {}
                client = AWSClient(sensor['host'],sensor['rootCAPath'],sensor['certificatePath'],sensor['privateKeyPath'],sensor['port'],sensor['clientId'],sensor['topic'])
                message['deviceId'] = sensor['deviceId']
                message['lat'] = sensor['lat']
                message['lng'] = sensor['lng']
                message['devicetimestamp']=str(datetime.datetime.now(timezone.utc))

                #Get new temp and humidty data in every 15 minutes
                #otherwise fail for rate limiting 
                if next_trigger<datetime.now():
                    humidity,temperature = OWP.get_humidity_temp(message['lat'],message['lng'])
                    next_trigger = self.__get_next_time(15)

                message['humidity'] = humidity
                message['moisture'] = float(random.normalvariate(99, 1.5))
                message['temperature'] = temperature
                message['sprinkler'] = sensor['sprinkler']
                message['farm'] = sensor['farm']
                messageJson = json.dumps(message)
                client.publish(messageJson,1)
                print('Published topic %s: %s\n' % (client.topic, message))

    def startSimulation(self):
        schedule.every(4).seconds.do(self.__startsensors)
        while 1:
            schedule.run_pending()
            time.sleep(5)


    
            
