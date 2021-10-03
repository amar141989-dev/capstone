from AwsCloudHelper import AwsCloudHelper
from datetime import timedelta
from datetime import datetime
from datetime import time
from datetime import timezone

from os.path import abspath
from DeviceConfiguration import DeviceConfiguration
from Simulator.Client.AWSClient import AWSClient

import schedule
import json
import random

from TableCreation import TableCreation
from RuleCreator import RuleCreator


print("Device Configuration Started")


invokeDeviceConfiguration=DeviceConfiguration()
invokeDeviceConfiguration.createThingType()

invokeDeviceConfiguration.createThingGroup()

invokeDeviceConfiguration.createThingSubGroup()

invokeDeviceConfiguration.createPolicy()

invokeDeviceConfiguration.createSprinklers()

invokeDeviceConfiguration.createSensors()

invokeDeviceConfiguration.downloadRootCa()

print("Device Configuration completed")


#This will create required dynamoDb tables
cTable=TableCreation()
cTable.startTableCreation()

#Create IOT type role manually.  (capstoneIoTRole)
#After creation add DynamoDbFullAccess 
#Note down arn 
#Create Rule for Inserting Data in DynamoDB Table
ruleCreator=RuleCreator()
ruleCreator.createRuleToPushRecordInDynamoDB()

