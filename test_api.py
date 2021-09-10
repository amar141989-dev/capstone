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
from AwsCloudHelper import AwsCloudHelper

ach=AwsCloudHelper("")

# resultThingType=ach.get_thing_type_list("");
# print("Type list: ",resultThingType)

# resultType = ach.create_thing_type("test_type","test_descr")
# print("Thing type: ", str(resultType))
# #print(ach.get_thing_type_list("test_type"))

# resultThingList=ach.get_thing_list("thing1","test_type");
# print("Thing list: ",resultThingList)

# resultThng= ach.create_thing("thing1","test_type")
# print("Thing with type: ", str(resultThng))

# resultThngGrp=ach.get_thing_group("SubTestGroup1","")
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
# resultPolicy=ach.create_topic("TestPolicy3");
# print("Policy: ",resultPolicy)

# resultAttachPolicy=ach.attach_policy_to_cert("TestPolicy3","arn:aws:iot:us-east-1:221389831253:cert/adeb5f32a8f68433b4e5fbacbe8d57160451c2fb29a4f236794d152833baa1a0");
# print("Attach policy: ",resultAttachPolicy)

# resultRule=ach.create_rule("dynamoInsert","Insert into dynamo using field split", "thng", "iot/moisture")
# print("Result rule: ",resultRule)


#---------------AWS API --End ----------------------------

