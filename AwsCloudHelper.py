from sys import dont_write_bytecode
import boto3
import os

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

    def create_thing_group(self, group_name, group_description, parent_group_name):
        response = None
        
        if(parent_group_name is None or len(parent_group_name)==0):
           response = self.iot_client.create_thing_group(
                thingGroupName=group_name,
                thingGroupProperties={
                    'thingGroupDescription':group_description,
                    } 
                )    
        else:
            response = self.iot_client.create_thing_group(
                thingGroupName=group_name,
                parentGroupName=parent_group_name,
                thingGroupProperties={
                    'thingGroupDescription':group_description,
                    }
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

    def create_topic(self, topic_name):
        response = self.iot_client.create_policy(
            policyName=topic_name,
            policyDocument="{\"Version\": \"2012-10-17\",\"Statement\": [{\"Effect\": \"Allow\",\"Action\": [\"*\"],\"Resource\": [\"*\"]}]}",
            tags=[
                {
                    'Key': 'junk',
                    'Value': 'junk'
                },
            ]
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
    
    #Parameters details are case sensitive 
    def create_rule(self, rule_name, rule_desc, table_name, topic_name):
        response = self.iot_client.create_topic_rule(
            ruleName=rule_name,
            topicRulePayload={
                'sql': "SELECT * FROM '" + topic_name + "'",
                'description': rule_desc,
                'actions': [
                    {
                        'dynamoDBv2': {
                            'roleArn': 'arn:aws:iam::221389831253:role/service-role/BSM_Dynamo_Role',
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
