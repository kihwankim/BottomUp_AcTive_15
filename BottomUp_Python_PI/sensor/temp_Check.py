import Adafruit_DHT
class Temp_Check:
    def solve():
        sensor = Adafruit_DHT.DHT11
        pin = 2
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if temperature is not None:
            if(temperature < 45):
                return True # Normal Situation
            else:
                return False # Emergency Situation
