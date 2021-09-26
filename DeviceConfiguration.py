from AwsCloudHelper import AwsCloudHelper
from datetime import timedelta
from datetime import datetime
from datetime import time
from datetime import timezone

from os.path import abspath
from Simulator.Client.AWSClient import AWSClient

import schedule
import json
import random

class DeviceConfiguration:
    def __init__(self):
        self.ach=AwsCloudHelper("")
        self.thing_policy="DevicePolicy"


# Create Thing Type (Device Type)
    def __getThingTypes(self):
        return  json.load(open(abspath('ConfigurationData\ThingType\DeviceType.json')))

    def __getThingGroups(self):
        return  json.load(open(abspath('ConfigurationData\ThingGroup\Customer.json'))) 

    def __getThingSubGroups(self):
        return  json.load(open(abspath('ConfigurationData\ThingSubGroup\Farms.json'))) 

    def __getAllSensors(self):
        return  json.load(open(abspath('ConfigurationData\Things\AllSensors.json'))) 

    def __getAllSprinklers(self):
        return  json.load(open(abspath('ConfigurationData\Things\AllSprinklers.json')))     
            
    def createThings(self):
        pass
# Create Thing Group (Customer Details)

    def createThingType(self):
        thingTypes = self.__getThingTypes()

        for tType in thingTypes:
            self.ach.create_thing_type(tType["typeName"],tType["typeDescription"])
            txt = "Thing type created {0} ".format(tType["typeName"])
            self.printLog(txt)


    def createThingGroup(self):
        thingGroups = self.__getThingGroups()

        for tGroup in thingGroups:
            self.ach.create_thing_group(tGroup["groupName"],tGroup["groupDescription"],"","","")
            txt = "Thing group created {0} ".format(tGroup["groupName"])
            self.printLog(txt)


    def createThingSubGroup(self):
        thingSubGroups = self.__getThingSubGroups()

        for tSubGroup in thingSubGroups:
            self.ach.create_thing_group(tSubGroup["subgroupName"],tSubGroup["groupDescription"],tSubGroup["groupName"],tSubGroup["lat"],tSubGroup["long"])                    
            txt = "Thing sub group created {0} in group {1} ".format(tSubGroup["subgroupName"],tSubGroup["groupName"])
            self.printLog(txt)

    def createPolicy(self):
        self.ach.create_policy(self.thing_policy)
        txt = "Policy created {0} ".format(self.thing_policy)
        self.printLog(txt)

    def createSprinklers(self):
        sprinklers = self.__getAllSprinklers()

        for sprinkler in sprinklers:
            self.ach.create_iot_thing(sprinkler["name"],sprinkler["type"], sprinkler["group"] + "\\" +sprinkler["subgroup"],self.thing_policy,"")
            txt = "Sprinkler created {0} ".format(sprinkler["name"])
            self.printLog(txt)

    def createSensors(self):
        sensors = self.__getAllSensors()

        for sensor in sensors:
            self.ach.create_iot_thing(sensor["name"],sensor["type"], sensor["group"] + "\\" +sensor["subgroup"],self.thing_policy,sensor["sprinkler"])
            txt = "Sensor created {0} ".format(sensor["name"])
            self.printLog(txt)

            txt = "Sensor {0} attached to sprinkler {1} ".format(sensor["name"],sensor["sprinkler"])
            self.printLog(txt)

    def createRootCA(self):
        self.ach.download_root_ca_if_not_exists()

    def printLog(self, message):
        print(message)

    def startDeviceConfiguration(self):
        print("Device Configuration Started")

        self.createThingType()

        self.createThingGroup()

        self.createThingSubGroup()

        self.createPolicy()

        self.createSprinklers()

        self.createSensors()

        print("Device Configuration completed")


# Create Thing Sub Group (Farm Details)
# Create Thing Policy 
# Create Thing (Devices like Sensors, Sprinklers)
