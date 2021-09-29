import constants
from AwsCloudHelper import AwsCloudHelper
class RuleCreator:

    def __init__(self) :
        self.ach=AwsCloudHelper("")

    def createRuleToPushRecordInDynamoDB(self):
        rule_name=constants.rule_name
        rule_desc=constants.rule_desc
        dynamo_table_name=constants.soil_sensor_data_alarmTableName
        topic_name=constants.topic_name
        iam_iot_role_arn=constants.iot_role_arn

        resultRule=self.ach.create_rule(rule_name, rule_desc, dynamo_table_name, topic_name, iam_iot_role_arn)

        print("Rule '{0}' Created Successfully".format(rule_name))