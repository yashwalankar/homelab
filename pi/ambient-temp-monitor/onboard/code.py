import time
import board
import adafruit_sht4x

i2c = board.I2C()
sht = adafruit_sht4x.SHT4x(i2c)

while True:
    temp, hum = sht.measurements
    print(f"{temp:.2f},{hum:.2f}")
    time.sleep(3)