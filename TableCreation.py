from DynamoTableCreation.CreateDynamoTables import CreateDynamoTables

class TableCreation:
    def __init__(self) -> None:
        self.cTable = CreateDynamoTables()
        pass

    def startTableCreation(self):

        print("Table  Creation Started")

        self.cTable.createSoilSensorAlarmTable()
        self.cTable.createSoilSensorDataTable()
        self.cTable.createSprinklerSwitchTable()
        self.cTable.createWeatherTable()


        print("Table  Creation completed")

    def startTableCleanup(self):

        print("Table  Cleanup Started")

        self.cTable.deleteAllTables()

        print("Table  Cleanup completed")

