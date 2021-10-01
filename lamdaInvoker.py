import boto3, json, typing
import schedule
from datetime import timedelta
from datetime import datetime
from datetime import timezone
import time
import constants
class LambdaInvoker:

    def invokeLambdaFunction(self, functionName:str=None, payload:typing.Mapping[str, str]=None):
        if  functionName == None:
            raise Exception('ERROR: functionName parameter cannot be NULL')
        payloadStr = json.dumps(payload)
        payloadBytesArr = bytes(payloadStr, encoding='utf8')
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName=functionName,
            InvocationType="RequestResponse",
            Payload=payloadBytesArr
        )
        return response

    def callLamdaCron(self):
        self.invokeLambdaFunction(constants.lambdaFunctionName,None)
        schedule.every(constants.lamdaCronDurationInMinute).seconds.do(self.invokeLambdaFunction(constants.lambdaFunctionName,None))
        while 1:
            schedule.run_pending()
            #this is to give pause for successful execution
            time.sleep(10)

