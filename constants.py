weather_dataTableName='weather_data'
soil_sensor_alarmTableName='soil_sensor_alarm'
soil_sensor_data_alarmTableName='soil_sensor_data'
sprinkler_switch_alarmTableName='sprinkler_switch'

topic_name ='iot/sensors'
port=8883
region_name ='us-east-1'

role_name='CapstoneEC2Role'
role_arn='arn:aws:iam::055670542642:role/CapstoneEC2Role'

rule_name='dynamoInsert'
rule_desc="Insert into dynamo using field split"


weather_api_key='151520a1bd651a75d263279a010f0baa'
