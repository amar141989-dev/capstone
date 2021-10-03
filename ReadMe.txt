# Install following modules 
#    > boto3
#    > requests
#    > aws client

# AWS Client Settings 
    #update credential file


# Manual action in AWS Console
    #Crreate Roles
        #capstoneDynamo Roles
            #List of policies
        #capstoneIoTRole
            #List of policies

    #create Lambda Function
        #code is available in  SprinklerMontiorlambda.py
        #attach role to Lambda function capstoneDynamoRole
#Device Configuration (One time Activity)
    #run InvokeDeviceConfiguration.py


# Start pushing sensor data using sensor simulatior
    #InvokeSensorSimulator.py

# Start receiving sprinkle alert
    #InvokeSensorSimulator.py

# Lambda Invoker
    #InvokeSensorSimulator.py

# Device Dashboard file
    #InvokeDeviceDashboard.py

