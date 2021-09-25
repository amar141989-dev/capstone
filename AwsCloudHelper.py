from sys import dont_write_bytecode
import boto3
import os
import requests

class AwsCloudHelper:

    def __init__(self, region_name):
        if region_name is None or len(region_name)==0:
            self.iot_client = boto3.client('iot',region_name ='us-east-1')
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

    def create_thing(self, thing_name, thing_type):
        response = self.iot_client.create_thing(
            thingName=thing_name,
            thingTypeName=thing_type
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

        if len(lat)==0 or len(lng)==0:
            raise Exception("Please specify the lat and long")

        tag_list.append({'Key': 'lat','Value': '' + lat + ''})
        tag_list.append({'Key': 'lng','Value': '' + lng + ''})
        
        if(parent_group_name is None or len(parent_group_name)==0):
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

        result={}
        
        result['thingGroupName']=response['thingGroupName']
        result['thingGroupArn']=response['thingGroupArn']

        result['thingGroupId']=response['thingGroupId']
        
        return result
        
        
        return response

    def create_thing_type(self, type_name, type_desc):
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
       
        return result

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
        response = self.iot_client.create_policy(
            policyName=policy_name,
            policyDocument="{\"Version\": \"2012-10-17\",\"Statement\": [{\"Effect\": \"Allow\",\"Action\": [\"*\"],\"Resource\": [\"*\"]}]}"
        )

        result={}
        result["policyName"]=response["policyName"]
        result["policyArn"]=response["policyArn"]
        result["policyVersionId"]=response["policyVersionId"]

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
    def create_rule(self, rule_name, rule_desc, table_name, topic_name, role_arn):
        response = self.iot_client.create_topic_rule(
            ruleName=rule_name,
            topicRulePayload={
                'sql': "SELECT * FROM '" + topic_name + "'",
                'description': rule_desc,
                'actions': [
                    {
                        'dynamoDBv2': {
                            'roleArn': role_arn,
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

    def create_iot_thing(self, thing_name, thing_type, thing_group, policy_name):

        response=self.get_thing_type_list(thing_type)
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

        response=self.create_thing(thing_name, thing_type)
        self.add_thing_to_thing_group(response["thingArn"],group_arn)

        resultCert = self.create_keys_and_certficate(thing_name)
        f= open('./Certificates/' +thing_name + '_certificate.pem.crt',"w+")
        f.write(resultCert["certificatePem"])
        f.close()

        f= open('./Certificates/' +thing_name + '_private.pem.key',"w+")
        f.write(resultCert["keyPair"]["PrivateKey"])
        f.close()

        f= open('./Certificates/' +thing_name + '_public.pem.key',"w+")
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
        response = self.iot_client.list_thing_groups_for_thing(
                    thingName=thing_name
                 )
        
        if len(response["thingGroups"])>0:
            tags["Farm"]=response["thingGroups"][0]["groupName"]
            locRes = self.get_resource_tags(response["thingGroups"][0]["groupArn"])
            tags.update(locRes) 
        
        
        tags["host"]="a3vifb8zgia71f-ats.iot.us-east-2.amazonaws.com"
        tags["rootCAPath"]="./Certificates/AmazonRootCA1.pem"
        tags["certificatePath"]="./Certificates/" +thing_name + "_certificate.pem.crt"
        tags["privateKeyPath"]="./Certificates/" +thing_name + "_public.pem.key"
        tags["port"]= 8883
        tags["topic"]= "iot/soilsensor"
        tags["deviceId"]=thing_name

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
        rootCaPath='./Certificates/AmazonRootCA1.pem'
        if not os.path.isfile(rootCaPath):
            if not os.path.exists(os.path.dirname(rootCaPath)):
                try:
                    os.makedirs(os.path.dirname(rootCaPath))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            rootCaUrl = 'https://www.amazontrust.com/repository/AmazonRootCA1.pem'
            r = requests.get(rootCaUrl, allow_redirects=True)
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