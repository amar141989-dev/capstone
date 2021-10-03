from DeviceDashboard import DeviceDashboard

dd=DeviceDashboard()
dd.getCustomerDetails("Spirit")
dd.getFarmDetails("AshleyFarm","Spirit")
dd.getSprinklerActuationSummary()
dd.getSprinklerActuationSummaryByName("Sprinkler2")
dd.getSensorDetails("IdealPlace")
