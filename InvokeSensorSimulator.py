from Simulator.DeviceSimulators.SensorSimulator import SensorSimulator
class InvokeSensorSimulator:
    def __init__(self) :
        pass

    def StartPushingSesorData(self):
        print("Sensor Simulation Started")
        sensorSimulator=SensorSimulator()
        sensorSimulator.startSimulation()
