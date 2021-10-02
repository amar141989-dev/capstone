weather_dataTableName='weather_data'
soil_sensor_alarmTableName='soil_sensor_alarm'
soil_sensor_data_alarmTableName='soil_sensor_data'
sprinkler_switch_alarmTableName='sprinkler_switch'

topic_name ='iot/sensors'
topic_name_for_subscribe='sprinkler/{0}'
port=8883
region_name ='us-east-1'

iot_role_name='capstoneIoTRole'
iot_role_arn='arn:aws:iam::221389831253:role/capstoneIoTRole'
# iot_role_arn='arn:aws:iam::055670542642:role/Capstone_DynDB'


rule_name='CapstoneDynamoRule'
rule_desc="Insert into dynamo using field split method"

absolute_certificate_path="./Certificates/"

aws_ca_root="https://www.amazontrust.com/repository/AmazonRootCA1.pem"

weather_api_key='151520a1bd651a75d263279a010f0baa'

lambdaFunctionName= 'sensorDataMonitor'
lamdaCronDurationInMinute=5

since_n_minutes_for_health_check=60
