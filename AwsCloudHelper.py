import boto3

class AwsCloudHelper:

    def __init__(self, region_name):
        if region_name is None or len(region_name)==0:
            self.iot_client = boto3.client('iot',region_name ='us-east-1')
        else:
            self.iot_client = boto3.client('iot',region_name)

    def add_thing_to_thing_group(self):
        pass

    def attach_policy(self):
        pass

    def create_policy(self):
        pass

    def create_thing(self):
        pass

    def create_thing_group(self, group_name, group_description, parent_group_name):
        response = self.iot_client.create_thing_group(
        thingGroupName=group_name,
        parentGroupName=parent_group_name,
        thingGroupProperties={
            'thingGroupDescription':group_description,
            # 'attributePayload': {
            #     'attributes': {
            #         'string': 'string'
            #     },
            #     'merge': True|False
            # }
        },
        tags=[
            {
                'Key': 'Test',
                'Value': 'GroupTest'
            },
            ]
        )
        return response

    def create_thing_type(self, type_name, type_desc):
        response = self.iot_client.create_thing_type(
        thingTypeName=type_name,
        thingTypeProperties={
            'thingTypeDescription': type_desc})
        return response

    def create_topic_rule(self):
        pass

    def create_keys_and_certficate(self):
        response = self.iot_client.create_keys_and_certificate(
            setAsActive=True|False
        )

        return response