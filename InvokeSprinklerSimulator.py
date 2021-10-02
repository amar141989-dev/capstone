from Simulator.DeviceSimulators.SprinklerSimulator import SprinklerSimulator
class InvokeSprinklerSimulator:
    def __init__(self) :
        pass

    def StartSubscribe(self):
        print("Sprinkler Simulation Started")
        sprinklerSimulator=SprinklerSimulator()
        sprinklerSimulator.startSimulation()
