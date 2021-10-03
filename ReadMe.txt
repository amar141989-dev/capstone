** Version 1.0.0
# Agri-Tech-Farm Water Management
----------------------------------------
# Install following python Packages 
#    > boto3 [command: pip install boto3]
#    > requests [command: pip install requests]
#    > AWSIoTPythonSDK [pip install AWSIoTPythonSDK] 
-------------------------------------------
# AWS Client Settings 
    > Go to C:\Users\<--UserName-->\.aws > credentials and update credentials
-------------------------------------------
# AWS Console Settings
    > Create IAM Roles mentioned below
        > capstoneDynamoRole
            > Permissions policies
                > AWSIoTThingsRegistration
                > AmazonDynamoDBFullAccess
                > AWSIoTRuleActions
                > AWSLambdaBasicExecutionRole
                > CloudWatchApplicationInsightsFullAccess
        > capstoneIoTRole
            > Permissions policies
               > AWSIoTThingsRegistration
               > AWSIoTLogging
               > AmazonDynamoDBFullAccess
               > AWSIoTRuleActions       
----------------------------------------------
# Create AWS Lambda Function
    > Code is available in  SprinklerMontiorlambda.py
    > Attach role to Lambda function capstoneDynamoRole
-----------------------------------------------
# One time activies
  > Device Configuration (One time Activity)
    > run InvokeDeviceConfiguration.py (It will in turn creates all the devices i.e Sensors and Sprinklers)
-----------------------------------------------
# Simulator
  > Start pushing sensor data using sensor simulatior
    > InvokeSensorSimulator.py

  > Start receiving sprinkler alert
    > InvokeSprinklerSimulator.py
------------------------------------------------
# Lambda Invoker
    #InvokeSensorSimulator.py
----------------------------------------------
# Device Dashboard file
    #InvokeDeviceDashboard.py
----------------------------------------------