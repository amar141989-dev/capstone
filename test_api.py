# from pyowm import OWM
# from pprint import pprint

# import json

# owm = OWM('151520a1bd651a75d263279a010f0baa')
# mgr = owm.weather_manager()
# one_call = mgr.one_call(lat=19.0485257,lon=72.8875786)
# current_data = json.dumps(one_call.current.__dict__)
# #pprint(current_data)
# print("Humidity: ", one_call.current.humidity, ", temperature: ", one_call.current.temperature('celsius')['temp']) # Eg.: 81

#---------------Open Weather Map API --Start ----------------------------
# from OpenWeatherMap import OpenWeatherMap

# owm=OpenWeatherMap("")
# print(owm.get_humidity_temp(19.0485257,72.8875786))
#---------------Open Weather Map API --End ----------------------------

#---------------AWS API --Start ----------------------------
import os
import re
from AwsCloudHelper import AwsCloudHelper
from database import Database

ach=AwsCloudHelper("")
db=Database()

# resultThingType=ach.get_thing_type_list("");
# print("Type list: ",resultThingType)

# resultType = ach.create_thing_type("test_type","test_descr")
# print("Thing type: ", str(resultType))
# #print(ach.get_thing_type_list("test_type"))

# resultThingList=ach.get_thing_list("","SoilSensor");
# print("Thing list: ",resultThingList)

# resultThng= ach.attach_device_to_thing("thing1","Sensor","Sprinkler1")
# print("Thing with type: ", str(resultThng))

# resultThngGrp=ach.get_thing_group("SubTestGroup1","TestGroup")
# print("Thing grp: ", resultThngGrp)

# #Gives error if already exists
# # resultGrp=ach.create_thing_group("TestGroup","TestDesc","")
# # print("Group: ", resultGrp)

# resultSubGrp1 = ach.create_thing_group("SubTestGroup1","TestDesc","TestGroup")
# print("Subgroup: ",resultSubGrp1)

# resultSubGrp2 = ach.create_thing_group("SubTestGroup2","TestDesc","TestGroup")
# print("Subgroup: ", resultSubGrp2)

# resultCert = ach.create_keys_and_certficate("thing")
# print("Cert: ", resultCert)

# thing="thing"
# f= open('./Certificates/' +thing + '_certificate.pem.crt',"w+")
# f.write(resultCert["certificatePem"])
# f.close()

# f= open('./Certificates/' +thing + '_private.pem.key',"w+")
# f.write(resultCert["keyPair"]["PrivateKey"])
# f.close()

# f= open('./Certificates/' +thing + '_public.pem.key',"w+")
# f.write(resultCert["keyPair"]["PublicKey"])
# f.close()

# resultPolicies = ach.list_policies()
# print("Policy: ", resultPolicies)

# #Gives already exists error 
# resultPolicy=ach.create_policy("TestPolicy3");
# print("Policy: ",resultPolicy)

# resultAttachPolicy=ach.attach_policy_to_cert("TestPolicy3","arn:aws:iot:us-east-1:221389831253:cert/adeb5f32a8f68433b4e5fbacbe8d57160451c2fb29a4f236794d152833baa1a0");
# print("Attach policy: ",resultAttachPolicy)

# resultRule=ach.create_rule("dynamoInsert","Insert into dynamo using field split", "thng", "iot/moisture","'arn:aws:iam::221389831253:role/service-role/BSM_Dynamo_Role'")
# print("Result rule: ",resultRule)


#---------------AWS API --End ----------------------------

# try:
#     thing_name="Device1"

#     thing_type="Sensor"
#     thing_type_desc="Soil sensors"
#     resultType = ach.create_thing_type(thing_type, thing_type_desc)
    
#     thing_group="AccountGrp1"
#     thing_group_desc="Account group description"
#     #Group can act as a account 
#     ach.create_thing_group(thing_group, thing_group_desc, "", "20", "30")

#     thing_sub_group="Farm1"
#     thing_sub_group_desc="Farm1 description"
#     #Group can act as a farm inside an account 
#     ach.create_thing_group(thing_sub_group, thing_sub_group_desc, thing_group, "20", "30")

#     thing_policy="DevicePolicy"
#     ach.create_policy(thing_policy)

#     #Create the thing and attach the specifed group, type and poliy to the thing
#     #It will also create certificates in the certicates folder      
#     result = ach.create_iot_thing(thing_name, thing_type, thing_group + "\\" + thing_sub_group, thing_policy)
    
#     print(ach.get_farm_tags_by_thing(thing_name))
    
#     rule_name="dynamoInsert"
#     rule_desc="Insert into dynamo using field split"
#     dynamo_table_name="thng"
#     topic_name="iot/moisture"
#     iam_role_arn="arn:aws:iam::221389831253:role/service-role/BSM_Dynamo_Role"

#     resultRule=ach.create_rule(rule_name, rule_desc, dynamo_table_name, topic_name, iam_role_arn)
#     print("Result rule: ",resultRule)
# except Exception as e:
#     print(e)

#ach.download_root_ca_if_not_exists()
# # print(ach.get_thing_list("","Sensor"))
# allSensors =ach.get_thing_list("","Sensor")
# allSensorsWithCert=[]
# for sensor in allSensors:
#     sensorWIthCA = ach.get_farm_tags_by_thing(sensor["thingName"])
#     allSensorsWithCert.append(sensorWIthCA)

# print(allSensorsWithCert)
# print(ach.get_farm_tags_by_thing("thing1"))
# print (ach.attach_device_to_thing("SoilSensor1","Sensor","Sprinkler1"))

# response=ach.get_group_details("IdealPlace")
# print(response)
# print("\n\n",response['thingGroupMetadata'])

# res={}
# res["groupName"]=response['thingGroupName']
# res["groupArn"]=response['thingGroupArn']

# if 'rootToParentThingGroups' in response['thingGroupMetadata']: 
#     res["parentGroupName"]=response['thingGroupMetadata']['rootToParentThingGroups'][0]['groupName']
#     res["parentGroupArn"]=response['thingGroupMetadata']['rootToParentThingGroups'][0]['groupArn']

# print("\n\n",res)

# import pathlib
# import constants 

# print(os.path.join(constants.absolute_certificate_path,"text.txt"))
# open(os.path.join(constants.absolute_certificate_path,"text.txt"),"w+").close()