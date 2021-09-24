from datetime import timedelta
from datetime import datetime
from datetime import time
from datetime import timezone

from os.path import abspath
from DeviceSimulators.OpenWeatherMap import OpenWeatherMap
from Client.AWSClient import AWSClient

import schedule
import json
import random

class SensorSimulator:

    def __init__(self):
        pass

    def __getsensors(self):
        return  json.load(open(abspath('E:/2021/AgriTech/capstone/Simulator/DataSource/Sensors.json')))

    def __get_next_time(self, interval_minutes):
        future_trigger_time = datetime.now() + timedelta(minutes=interval_minutes)
        return future_trigger_time
    
    def __startsensors(self):
        #get sensors
        sensors = self.__getsensors()
        OWP = OpenWeatherMap('151520a1bd651a75d263279a010f0baa')
        next_trigger = self.__get_next_time(-1)
        humidity, temperature = (0,0)
        while True:
            for sensor in sensors:
                message = {}
                client = AWSClient(sensor['host'],sensor['rootCAPath'],sensor['certificatePath'],sensor['privateKeyPath'],sensor['port'],sensor['clientId'],sensor['topic'])
                message['deviceId'] = sensor['deviceId']
                message['lat'] = sensor['lat']
                message['lon'] = sensor['lon']
                message['devicetimestamp']=str(datetime.datetime.now(timezone.utc))

                #Get new temp and humidty data in every 15 minutes
                #otherwise fail for rate limiting 
                if next_trigger<datetime.now():
                    humidity,temperature = OWP.get_humidity_temp(message['lat'],message['lon'])
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


    
            
