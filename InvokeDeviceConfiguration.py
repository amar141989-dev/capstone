from DeviceConfiguration import DeviceConfiguration
from TableCreation import TableCreation
from RuleCreator import RuleCreator

#Below code will start device configuration
dconfig=DeviceConfiguration()
dconfig.startDeviceConfiguration()
dconfig.downloadRootCa()

#This will create required dynamoDb tables
cTable=TableCreation()
# cTable.startTableCreation()

#Create IOT type role manually.  (capstoneIoTRole)
#After creation add DynamoDbFullAccess 
#Note down arn 
#Create Rule for Inserting Data in DynamoDB Table
ruleCreator=RuleCreator()
ruleCreator.createRuleToPushRecordInDynamoDB()
