from re import S
from sys import dont_write_bytecode
from types import resolve_bases
import boto3
import os
import requests
from botocore.exceptions import ClientError
import constants

class AwsCloudHelper:

    def __init__(self, region_name):
        if region_name is None or len(region_name)==0:
            self.iot_client = boto3.client('iot',region_name =constants.region_name)
        else:
            self.iot_client = boto3.client('iot',region_name)

    def add_thing_to_thing_group(self, thing_name_arn, thing_group_arn):
        response = self.iot_client.add_thing_to_thing_group(
            thingGroupArn=thing_group_arn,
            thingArn=thing_name_arn
        )

        return response

    def attach_policy(self):
        pass

    def create_policy(self):
        pass

    def create_thing(self, thing_name, thing_type,attributePayloadData):
        response = self.iot_client.create_thing(
            thingName=thing_name,
            thingTypeName=thing_type,
            attributePayload=attributePayloadData

        )
        result={}
        result['thingName']=response['thingName']
        result['thingArn']=response['thingArn']
        result['thingId']=response['thingId']
        
        return result

    def create_thing_group(self, group_name, group_description, parent_group_name, lat, lng):
        response = None
        tag_list=[]

        if len(group_name)==0:
            raise Exception("Please specify the group name.")

        if len(parent_group_name)!=0 and (len(str(lat))==0 or len(str(lng))==0):
            raise Exception("Please specify the lat and long")

       
        tag_list.append({'Key': 'lat','Value': '' + str(lat) + ''})
        tag_list.append({'Key': 'lng','Value': '' + str(lng) + ''})

        if len (parent_group_name)==0:
            tag_list=[]
        
        #to be return
        result={}

        try:

        
            if(parent_group_name is None or len(parent_group_name)==0):

                #get thing group if already 
                response = self.iot_client.create_thing_group(
                        thingGroupName=group_name,
                        thingGroupProperties={
                            'thingGroupDescription':group_description,
                            },
                            tags=tag_list 
                        )    
            else:
                response = self.iot_client.create_thing_group(
                    thingGroupName=group_name,
                    parentGroupName=parent_group_name,
                    thingGroupProperties={
                        'thingGroupDescription':group_description,
                        },
                        tags=tag_list
                    )    
            result['thingGroupName']=response['thingGroupName']
            result['thingGroupArn']=response['thingGroupArn']

            result['thingGroupId']=response['thingGroupId']
           
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print("Resource {0} already exists".format(group_name))
                responseForThing = self.get_thing_group(group_name,parent_group_name)

                result['thingGroupName']=responseForThing[0]['groupName']
                result['thingGroupArn']=responseForThing[0]['groupArn']

            else:
                print("Unexpected error: %s" % e)
            
    
        

        
        return result
        
        
        return response

    def create_thing_type(self, type_name, type_desc):
        try:
            
            response = self.iot_client.create_thing_type(
                    thingTypeName=type_name,
                    thingTypeProperties={
                        'thingTypeDescription': type_desc
                        }
                    )
            result={}
            result["thingTypeName"]=response["thingTypeName"]
            result["thingTypeArn"]=response["thingTypeArn"]
            result["thingTypeId"]=response["thingTypeId"]

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print("Thing type {0} already exists".format(type_name))

                response=   self.get_thing_type(type_name)
                # print(response)
                result={}
                result["thingTypeName"] =response[0]["thingTypeName"]
                result["thingTypeArn"]=response[0]["thingTypeArn"]

            else:
                print("Unexpected error: %s" % e)

       
        return result

    def deleteAll_thing_type(self, type_name, type_desc):
        try:
            
            response = self.iot_client.list_thing_types()
            if len(response["thingTypes"])>0:
                for thingType in response["things"]:
                    self.iot_client.delete_thing_type(thingType["thingTypeName"])

        except ClientError as e:
            print("Unexpected error: %s" % e)


    def create_topic_rule(self):
        pass

    def create_keys_and_certficate(self,thing_name):
        response = self.iot_client.create_keys_and_certificate(
            setAsActive=True
        )

        return response

    def get_thing_type_list(self, thing_type_name):
        response =  None 
        
        if thing_type_name is None or len(thing_type_name)==0:
            response = self.iot_client.list_thing_types()
        else:
            response = self.iot_client.list_thing_types(thingTypeName=thing_type_name)

        return response["thingTypes"]

    def get_thing_type(self, thing_type_name):
        response=None 
        response = self.iot_client.list_thing_types(thingTypeName=thing_type_name)
        return response["thingTypes"]


    def get_thing_list(self, thing_name, thing_type_name):
        response = None

        if thing_type_name is None or len(thing_type_name)==0:
            response = self.iot_client.list_things()
        else:
            response = self.iot_client.list_things(thingTypeName=thing_type_name)

        if len(thing_name)>0:
            thingList=[]
            for thing in response["things"]:
               if thing_name==thing["thingName"]:
                   thingList.append(thing)

            return thingList

        return response["things"]
    
    def get_thing_group(self, group_name, parent_group_name):
        response=None 
        if parent_group_name is None or len(parent_group_name)==0:
            response = self.iot_client.list_thing_groups()
        else:
            response = self.iot_client.list_thing_groups(parentGroup=parent_group_name)
        
        if len(group_name)>0:
            grpList=[]
            for grp in response["thingGroups"]:
                if group_name==grp["groupName"]:
                    grpList.append(grp)
            return grpList
            
        return response["thingGroups"]

    def create_policy(self, policy_name):
        result={}

        try:
                
            response = self.iot_client.create_policy(
                policyName=policy_name,
                policyDocument="{\"Version\": \"2012-10-17\",\"Statement\": [{\"Effect\": \"Allow\",\"Action\": [\"*\"],\"Resource\": [\"*\"]}]}"
            )

            result["policyName"]=response["policyName"]
            result["policyArn"]=response["policyArn"]
            result["policyVersionId"]=response["policyVersionId"]

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print("Policy {0} already exists".format(policy_name))

                result["policyName"]=policy_name

            else:
                print("Unexpected error: %s" % e)

        return result
    
    def attach_policy_to_cert(self, policy_name, certificate_name):
        response = self.iot_client.attach_policy(
                policyName=policy_name,
                target=certificate_name
            )

        return response
    
    def list_policies(self):
        response = self.iot_client.list_policies(ascendingOrder=True)
        return response["policies"]
    

    #Parameters details are case sensitive 
    def create_rule(self, rule_name, rule_desc, table_name, topic_name, iot_role_arn):

        response = self.iot_client.create_topic_rule(
            ruleName=rule_name,
            topicRulePayload={
                'sql': "SELECT * FROM '" + topic_name + "'",
                'description': rule_desc,
                'actions': [
                    {
                        'dynamoDBv2': {
                            'roleArn': iot_role_arn,
                            'putItem': {
                                'tableName': table_name
                            }
                        }
                    },
                ],
                'ruleDisabled': False
            }
        )    

        return response["ResponseMetadata"]["RequestId"]   

    def create_root_ca(self):
        pass

    def create_iot_thing(self, thing_name, thing_type, thing_group, policy_name, thing_attachedDevice):

        response=self.get_thing_type_list(thing_type)

        #create directory fro certificates
        if not os.path.exists(os.path.dirname(constants.absolute_certificate_path)):
            try:
                os.makedirs(os.path.dirname(constants.absolute_certificate_path))
                print("Certificate directory created")
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        if not response:
            raise Exception("Specified thing type does not exists.")

        group_arn=""
        if len(thing_group)>0:
            groups=thing_group.split("\\")
            group=None
            if len(groups)==1:
                group=self.get_thing_group(groups[0],"")
            else:
                group=self.get_thing_group(groups[1],groups[0])
            
            if not group:
                raise Exception("Specified thing group does not exists.")
            else:
                group_arn=group[0]["groupArn"]

        attributePayloadData={}

        if(len(thing_attachedDevice) > 0):
            attributePayloadData={
                'attributes': {
                    'sprinkler': thing_attachedDevice
                },
                'merge': True
            }

        response=self.create_thing(thing_name, thing_type, attributePayloadData)
        self.add_thing_to_thing_group(response["thingArn"],group_arn)

        resultCert = self.create_keys_and_certficate(thing_name)
        filePath=os.path.join(constants.absolute_certificate_path, thing_name + '_certificate.pem.crt')
        f= open(filePath,"w+")
        f.write(resultCert["certificatePem"])
        f.close()

        filePath=os.path.join(constants.absolute_certificate_path, thing_name + '_private.pem.key')
        f= open(filePath,"w+")
        f.write(resultCert["keyPair"]["PrivateKey"])
        f.close()

        filePath=os.path.join(constants.absolute_certificate_path, thing_name + '_public.pem.key')
        f= open(filePath,"w+")
        f.write(resultCert["keyPair"]["PublicKey"])
        f.close()
        
        self.attach_policy_to_cert(policy_name, resultCert["certificateArn"])
        self.attach_policy_to_cert(policy_name, group_arn)

        self.iot_client.attach_thing_principal(thingName=thing_name, principal=resultCert["certificateArn"])
        return response
    
    def get_farm_tags_by_thing(self, thing_name):
        response = self.iot_client.describe_thing(
                thingName=thing_name
            )
        tags=response["attributes"]
        tags["deviceType"]=response["thingTypeName"]
        
        response = self.iot_client.list_thing_groups_for_thing(
                    thingName=thing_name
                 )
        
        if len(response["thingGroups"])>0:
            tags["Farm"]=response["thingGroups"][0]["groupName"]
            locRes = self.get_resource_tags(response["thingGroups"][0]["groupArn"])
            tags.update(locRes) 
        
        
        tags["rootCAPath"]="AmazonRootCA1.pem"
        tags["certificatePath"]=thing_name + "_certificate.pem.crt"
        tags["privateKeyPath"]=thing_name + "_private.pem.key"
        tags["port"]= constants.port
        tags["topic"]= constants.topic_name
        tags["deviceId"]=thing_name

        response = self.iot_client.describe_endpoint(endpointType="iot:Data-ATS")
        
        tags["host"]=response["endpointAddress"]

        groupDetail = self.get_group_details(tags["Farm"])
        if 'parentGroupName' in groupDetail:
            tags["clientId"]=groupDetail["parentGroupName"]
            
        return tags

    def get_resource_tags(self, arn):
        locRes = self.iot_client.list_tags_for_resource(
                        resourceArn=arn
                    )
        response={}
        for key in locRes["tags"]:
            response[key["Key"]]=key["Value"]

        return response

    def download_root_ca_if_not_exists(self):
        absPath = os.path.abspath(constants.absolute_certificate_path)

        rootCaPath=os.path.join(absPath,'AmazonRootCA1.pem')
        if not os.path.isfile(rootCaPath):
            if not os.path.exists(os.path.dirname(rootCaPath)):
                try:
                    os.makedirs(os.path.dirname(rootCaPath))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            
            r = requests.get(constants.aws_ca_root, allow_redirects=True)
            f= open(rootCaPath,"wb")
            f.write(r.content)
            f.close()
    
    def attach_device_to_thing(self, thing_name, thing_type, device_name):
        response = self.iot_client.create_thing(
            thingName=thing_name,
            thingTypeName=thing_type,
            attributePayload={
                'attributes': {
                    'sprinkler': device_name
                },
                'merge': True
            }
        )
        result={}
        result['thingName']=response['thingName']
        result['thingArn']=response['thingArn']
        result['thingId']=response['thingId']
        
        return result
    
    def get_group_details(self, group_name):
        response = self.iot_client.describe_thing_group(thingGroupName=group_name)
        result={}
        result["groupName"]=response['thingGroupName']
        result["groupArn"]=response['thingGroupArn']

        if 'rootToParentThingGroups' in response['thingGroupMetadata']: 
            result["parentGroupName"]=response['thingGroupMetadata']['rootToParentThingGroups'][0]['groupName']
            result["parentGroupArn"]=response['thingGroupMetadata']['rootToParentThingGroups'][0]['groupArn']
        
        return result
    
    def list_things_in_thing_group(self, group_name):
        response = self.iot_client.list_things_in_thing_group(thingGroupName=group_name)
        return response; 