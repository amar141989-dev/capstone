import sys
from pyowm import OWM

class OpenWeatherMap:

    def __init__(self, secret_key):
        owm=None
        if secret_key is None or len(secret_key) == 0:
            owm = OWM('151520a1bd651a75d263279a010f0baa')
        else:
            owm=OWM(secret_key)

        self.mgr = owm.weather_manager()

    def get_humidity_temp(self, lat, lon):
        one_call = self.mgr.one_call(lat, lon)
        humidity=one_call.current.humidity
        temperature=one_call.current.temperature('celsius')['temp']
        return (humidity, temperature)