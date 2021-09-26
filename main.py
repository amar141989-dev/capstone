from TableCreation import TableCreation
from DeviceConfiguration import DeviceConfiguration
from DynamoTableCreation.CreateDynamoTables import CreateDynamoTables
from CleanUpScript import CleanUpScript
from RuleCreator import RuleCreator
from InvokeSensorSimulator import InvokeSensorSimulator

#Cleanup Script
dCleanUp=CleanUpScript()
# dCleanUp.startClenUp()


#Below code will start device configuration
dconfig=DeviceConfiguration()
# dconfig.startDeviceConfiguration()


#This will create required dynamoDb tables
cTable=TableCreation()
# cTable.startTableCreation()


#Create Rule for Inserting Data in DynamoDB Table
ruleCreator=RuleCreator()
ruleCreator.createRuleToPushRecordInDynamoDB()


#Push Data to Dynamo  table using simulator
invokeSensorSimulator=InvokeSensorSimulator()
invokeSensorSimulator.StartPushingSesorData()
