from AwsCloudHelper import AwsCloudHelper

class DeviceDashboard:
    def __init__(self) :
        self.ach=AwsCloudHelper("")

        pass
    def getCustomerDetails(self, customerName):
        print("Getting Customer Details")
        res=self.ach.get_thing_group("",customerName)
        print("{: <20} {: <20} {: <20} {: <20}".format("Farm Name","Customer Name", "lat", "lng"))

        for grp in res:
            grpDtl=self.ach.get_group_details(grp["groupName"])
            groupName=grpDtl['groupName']
            parentGroupName="-"
            lat=""
            lng=""
            if 'parentGroupName' in grpDtl:
                parentGroupName=grpDtl['parentGroupName']
                locRes = self.ach.get_resource_tags(grpDtl["groupArn"])
                lat=str(locRes["lat"])
                lng=str(locRes["lng"])
                
            print("{: <20} {: <20} {: <20} {: <20}".format(grp["groupName"],parentGroupName, lat, lng))
        pass

    def getFarmDetails(self, farmName, customerName):
        print("Getting Farm Details")

        res=self.ach.get_thing_group(farmName,customerName)
        print("{: <20} {: <20} {: <20} {: <20}".format("Farm Name","Customer Name", "lat", "lng"))

        for grp in res:
            grpDtl=self.ach.get_group_details(grp["groupName"])
            groupName=grpDtl['groupName']
            parentGroupName="-"
            lat=""
            lng=""
            if 'parentGroupName' in grpDtl:
                parentGroupName=grpDtl['parentGroupName']
                locRes = self.ach.get_resource_tags(grpDtl["groupArn"])
                lat=str(locRes["lat"])
                lng=str(locRes["lng"])
                
            print("{: <20} {: <20} {: <20} {: <20}".format(grp["groupName"],parentGroupName, lat, lng))
        pass

    def getSensorDetails(self, deviceName):
        #connect dyanamo and get latest timestamp when data received
        #derive health of sensor
        #show recent sensor data received
        pass

    def getSprinklerActuationSummary(self):
        pass

    def getSprinklerActuationSummaryById(self, sprinklerID):
        pass