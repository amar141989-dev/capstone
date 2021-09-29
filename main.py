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
dconfig.startDeviceConfiguration()
dconfig.downloadRootCa()

#This will create required dynamoDb tables
cTable=TableCreation()
cTable.startTableCreation()


#Create IOT type role manually.  (capstoneIoTRole)
#After creation add DynamoDbFullAccess 
#Note down arn 
#Create Rule for Inserting Data in DynamoDB Table
ruleCreator=RuleCreator()
ruleCreator.createRuleToPushRecordInDynamoDB()

#Download the root CA certificates


#Push Data to Dynamo  table using simulator
invokeSensorSimulator=InvokeSensorSimulator()
invokeSensorSimulator.StartPushingSensorData()
