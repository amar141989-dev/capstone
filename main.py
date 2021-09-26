from TableCreation import TableCreation
from DeviceConfiguration import DeviceConfiguration
from DynamoTableCreation.CreateDynamoTables import CreateDynamoTables
from CleanUpScript import CleanUpScript

#Cleanup Script
dCleanUp=CleanUpScript()
dCleanUp.startClenUp()


#Below code will start device configuration
# dconfig=DeviceConfiguration()
# dconfig.startDeviceConfiguration()


#This will create required dynamoDb tables
cTable=TableCreation()
cTable.startTableCreation()


