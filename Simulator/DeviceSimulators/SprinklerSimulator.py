import json
import os

from os.path import abspath
from Simulator.Client.AWSClient import AWSClient
import schedule
import time
from AwsCloudHelper import AwsCloudHelper
import constants

class SprinklerSimulator:

    def __init__(self):
        self.ach=AwsCloudHelper("")
        self.allSprinklersWithCert=[]
        pass

    def __getsprinklers(self):
        if len(self.allSprinklersWithCert)==0:
            allSprinklers =self.ach.get_thing_list("","Sprinkler")
            for sprinkler in allSprinklers:
                sprinklerWIthCA = self.ach.get_farm_tags_by_thing(sprinkler["thingName"])
                self.allSprinklersWithCert.append(sprinklerWIthCA)

        print("Avaialble sprinklers count is {0}", len(self.allSprinklersWithCert))
    
    def __startSprinklerSubscriptions(self):
        print('BEGIN __startSprinklerSubscriptions')
        sprinklers = self.__getsprinklers()
        for sprinkler in self.allSprinklersWithCert:
            # client = AWSClient(sprinkler['host'],sprinkler['rootCAPath'],sprinkler['certificatePath'],sprinkler['privateKeyPath'],sprinkler['port'],sprinkler['clientId'],sprinkler['topic']+sprinkler['deviceId'])
            
            host=sprinkler['host']
            rootCAPath=os.path.join(constants.absolute_certificate_path, sprinkler['rootCAPath'])
            certificatePath=os.path.join(constants.absolute_certificate_path, sprinkler['certificatePath'])
            privateKeyPath=os.path.join(constants.absolute_certificate_path, sprinkler['privateKeyPath'])
            port=sprinkler['port']
            clientId=sprinkler['clientId']
            topic=constants.topic_name_for_subscribe.format(sprinkler['deviceId']) 
            
            client = AWSClient(host, rootCAPath, certificatePath, privateKeyPath, port, clientId, topic)
            client.subscribe(1, self.customCallback)
            
    def customCallback(self,client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    def startSimulation(self):
        self.__startSprinklerSubscriptions()
        schedule.every(300).seconds.do(self.__startSprinklerSubscriptions)
        while 1:
            schedule.run_pending()
            time.sleep(5)




