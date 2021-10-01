from TableCreation import TableCreation
from DeviceConfiguration import DeviceConfiguration
from DynamoTableCreation.CreateDynamoTables import CreateDynamoTables
from CleanUpScript import CleanUpScript
from RuleCreator import RuleCreator
from InvokeSensorSimulator import InvokeSensorSimulator
from lamdaInvoker import LambdaInvoker 
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
#invokeSensorSimulator.StartPushingSensorData()


#create lambda function manually. Lambda Function Name :- sensorDataMonitor
#event bridge creation needs permission. AWS educate account does not have permission.
# Workaround for this is create python script to invoke python script
#create event bridge rule with name  triggerSensorDataMonitor, this will trigger lambda fnction every 5 min.
#trigger Name :- triggerSensorDataMonitor
#trigger description : This will trigger lamda function every 5 min. 
#schedule expression : rate(5 minutes)


#alternate option for event bridge. 
#create python script and execute it every five minutes

callLambda =LambdaInvoker ()
callLambda.callLamdaCron()

#Run Sprinkler simulator to receive alerts to ON OFF sprinkler from Lamda 



