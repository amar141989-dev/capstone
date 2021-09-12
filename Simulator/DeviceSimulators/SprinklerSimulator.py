import json
from os.path import abspath
from Client.AWSClient import AWSClient
import schedule
import time

class SprinklerSimulator:

    def __init__(self) -> None:
        pass

    def __getsprinklers(self):
        return  json.load(open(abspath('E:/2021/AgriTech/capstone/Simulator/DataSource/Sprinklers.json')))

    def __startSprinklerSubscriptions(self):
        sprinklers = self.__getsprinklers()
        for sprinkler in sprinklers:
            client = AWSClient(sprinkler['host'],sprinkler['rootCAPath'],sprinkler['certificatePath'],sprinkler['privateKeyPath'],sprinkler['port'],sprinkler['clientId'],sprinkler['topic']+sprinkler['deviceId'])
            client.subscribe(1, self.customCallback)
            
    def customCallback(self,client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    def startSimulation(self):
        schedule.every(4).seconds.do(self.__startSprinklerSubscriptions)
        while 1:
            schedule.run_pending()
            time.sleep(5)




