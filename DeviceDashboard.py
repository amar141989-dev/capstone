from AwsCloudHelper import AwsCloudHelper
from database import Database
import constants

class DeviceDashboard:
    def __init__(self) :
        self.ach=AwsCloudHelper("")
        self.db=Database()

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

    def getSensorDetails(self, farmName):
        #connect dyanamo and get latest timestamp when data received
        #derive health of sensor
        #show recent sensor data received
        res=self.ach.list_things_in_thing_group(farmName)
        devices=[]
        things=[]
        things=res["things"]
        # things.append("SoilSensor1")
        for thing in things:
            dtl=self.ach.get_farm_tags_by_thing(thing)
            dtl["status"]="Unhealthy"#get_device_status(thing)
            res=self.db.get_data_since_by_key(constants.soil_sensor_data_alarmTableName, thing, constants.since_n_minutes_for_health_check)
            if(len(res)>0):
                dtl["status"]="Healthy"

            devices.append(dtl)

        print("{: <20} {: <20} {: <20} {: <20} {: <20}".format("Account Name", "Farm", "DeviceId",  "DeviceType", "Status"))
        for device in devices:
            print("{: <20} {: <20} {: <20} {: <20} {: <20}".format(dtl["clientId"], dtl["Farm"], dtl["deviceId"],  dtl["deviceType"], dtl["status"]))

    def getSprinklerActuationSummary(self):
        # get details when this sprinkler get invoked table soil_sensor_alarm
        res=self.db.get_data(constants.soil_sensor_alarmTableName, 100)
        print("{: <20} {: <20} {: <20}".format("DeviceId","Action", "Timestamp"))
        for item in res:
            print("{: <20} {: <20} {: <20}".format(item['deviceid']['S'],item['action']['S'],item['alarmtimestamp']['S']))


    def getSprinklerActuationSummaryByName(self, sprinklerName):
        res=self.db.get_data_by_key(constants.soil_sensor_alarmTableName, sprinklerName)
        print("{: <20} {: <20} {: <20}".format("DeviceId","Action", "Timestamp"))
        for item in res:
            print("{: <20} {: <20} {: <20}".format(item['deviceid']['S'],item['action']['S'],item['alarmtimestamp']['S']))