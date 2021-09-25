from DeviceConfiguration import DeviceConfiguration

#start device configuration.
print("Device Configuration Started")

dconfig=DeviceConfiguration()

dconfig.createThingType()

dconfig.createThingGroup()

dconfig.createThingSubGroup()

dconfig.createPolicy()

dconfig.createSprinklers()

dconfig.createSensors()


print("Device Configuration completed")