from TableCreation import TableCreation
class CleanUpScript:

    def startClenUp(self):
        #Cleanup dynamo tables
        tCleanup=TableCreation()
        tCleanup.startTableCleanup()

