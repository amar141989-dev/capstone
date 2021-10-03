import boto3, json, typing
import schedule
from datetime import timedelta
from datetime import datetime
from datetime import timezone
import time
import constants
class LambdaFunctionCaller:

    def invokeLambdaFunction(self):
        payloadStr = json.dumps(None)
        payloadBytesArr = bytes(payloadStr, encoding='utf8')
        client = boto3.client('lambda')
        response = client.invoke(   
            FunctionName=constants.lambdaFunctionName,
            InvocationType="RequestResponse",
            Payload=payloadBytesArr
        )
        return response

    def callLamdaCron(self):
        self.invokeLambdaFunction()
        schedule.every(constants.lamdaCronDurationInMinute).seconds.do(self.invokeLambdaFunction)
        while 1:
            schedule.run_pending()
            #this is to give pause for successful execution
            time.sleep(10)

