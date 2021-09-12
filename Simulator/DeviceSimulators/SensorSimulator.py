from datetime import time
from os.path import abspath
import json
from DeviceSimulators.OpenWeatherMap import OpenWeatherMap
from Client.AWSClient import AWSClient
import schedule
import time
import datetime

class SensorSimulator:

    def __init__(self):
        pass

    def __getsensors(self):
        return  json.load(open(abspath('E:/2021/AgriTech/capstone/Simulator/DataSource/Sensors.json')))

    def __startsensors(self):
        #get sensors
        sensors = self.__getsensors()
        OWP = OpenWeatherMap('151520a1bd651a75d263279a010f0baa')
        for sensor in sensors:
            message = {}
            client = AWSClient(sensor['host'],sensor['rootCAPath'],sensor['certificatePath'],sensor['privateKeyPath'],sensor['port'],sensor['clientId'],sensor['topic'])
            message['deviceId'] = sensor['deviceId']
            message['lat'] = sensor['lat']
            message['lon'] = sensor['lon']
            message['devicetimestamp']=str(datetime.datetime.now())
            humidity,temperature = OWP.get_humidity_temp(message['lat'],message['lon'])
            message['humidity'] = humidity
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


    
            
