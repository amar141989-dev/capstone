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
from OpenWeatherMap import OpenWeatherMap

owm=OpenWeatherMap("")
print(owm.get_humidity_temp(19.0485257,72.8875786))
#---------------Open Weather Map API --End ----------------------------

#---------------AWS API --Start ----------------------------
from AwsCloudHelper import AwsCloudHelper

ach=AwsCloudHelper("")

# resultThingType=ach.get_thing_type_list("");
# print("Type list: ",resultThingType)

# resultType = ach.create_thing_type("test_type","test_descr")
# print("Thing type: ", str(resultType))
# #print(ach.get_thing_type_list("test_type"))

resultThingList=ach.get_thing_list("","SoilSensor");
print("Thing list: ",resultThingList)

# resultThng= ach.create_thing("thing1","test_type")
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

# resultRule=ach.create_rule("dynamoInsert","Insert into dynamo using field split", "thng", "iot/moisture")
# print("Result rule: ",resultRule)


#---------------AWS API --End ----------------------------

# try:
#     print("1")
#     thing_name="thing1"

#     thing_type="TestType1"
#     thing_type_desc="Test description"
#     resultType = ach.create_thing_type(thing_type, thing_type_desc)
#     print("2")

#     thing_group="TestGroup"
#     thing_group_desc="Thing group description"
#     ach.create_thing_group(thing_group, thing_group_desc, "")
#     print("3")

#     thing_sub_group="SubTestGroup1"
#     thing_sub_group_desc="SubTestGroup1 description"
#     ach.create_thing_group(thing_sub_group, thing_sub_group_desc, thing_group)
#     print("4")

#     thing_policy="ThingPolicy"
#     ach.create_policy(thing_policy);
#     print("5")

#     result = ach.create_iot_thing(thing_name, thing_type, thing_group + "\\" + thing_sub_group, thing_policy)
#     print("6")

#     print(result)
# except Exception as e:
#     print(e)
