import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException
from AWSIoTPythonSDK.core.protocol.internal.defaults import DEFAULT_OPERATION_TIMEOUT_SEC
from botocore.exceptions import ClientError


class AWSClient:

    def __init__(self,host,rootCAPath,certificatePath,privateKeyPath,port,clientId,topic):
        self.logger = self.__getLogger()
        self.topic = topic
        self.AWSMQTTClient = self.__getmyAWSIoTMQTTClient(host,rootCAPath,certificatePath,privateKeyPath,port,clientId)

    def __getLogger(self):
        # Configure logging
        logger = logging.getLogger("AWSIoTPythonSDK.core")
        logger.setLevel(logging.DEBUG)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        return logger

    def __getmyAWSIoTMQTTClient(self,host,rootCAPath,certificatePath,privateKeyPath,port,clientId):
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
        # AWSIoTMQTTClient connection configuration
        myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        return myAWSIoTMQTTClient

    def publish(self,messageJson,Qos):
        try:

            self.AWSMQTTClient.connect()
            self.AWSMQTTClient.publish(self.topic, messageJson, 1)
        except ClientError as e:
            print("Publsh failed Message {0}".format(messageJson))
            print("Unexpected error: %s" % e) 

    def subscribe(self,Qos,customCallback):
        self.AWSMQTTClient.connect()
        self.AWSMQTTClient.subscribe(self.topic, Qos, customCallback)