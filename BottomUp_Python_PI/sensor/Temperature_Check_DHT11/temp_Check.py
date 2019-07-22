import Adafruit_DHT
def check_Temperature():
    # 일정 온도가 넘어가지 않을 시 True를 반환, 온도 넘어가면 False를 반환
    # Normal Situation 에서는 True, Emergency Situation 에서는 False를 반환
    sensor = Adafruit_DHT.DHT11
    pin = 17
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if temperature is not None:
        if(temperature < 30):
            return True # Normal Situation
        else:
            return False # Emergency Situation