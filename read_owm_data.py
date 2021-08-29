from pyowm import OWM
from pprint import pprint

import json

owm = OWM('151520a1bd651a75d263279a010f0baa')
mgr = owm.weather_manager()
one_call = mgr.one_call(lat=19.0485257,lon=72.8875786)
current_data = json.dumps(one_call.current.__dict__)
#pprint(current_data)
print("Humidity: ", one_call.current.humidity, ", temperature: ", one_call.current.temperature('celsius')['temp']) # Eg.: 81
