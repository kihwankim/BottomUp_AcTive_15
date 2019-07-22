import Adafruit_DHT
class Temp_Check:
    def check_Temperature(self):
        sensor = Adafruit_DHT.DHT11
        pin = 17
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if temperature is not None:
            if(temperature < 30):
                return True # Normal Situation
            else:
                return False # Emergency Situation