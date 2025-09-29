import os
import time
import csv
import serial
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# Configuration
com_port = os.getenv('SERIAL_PORT', '/dev/cu.usbmodem2101') # Default port to run and test directly on mac, outside docker
baud_rate = os.getenv('BAUD_RATE', '115200')  

# InfluxDB v2 Configuration
INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://192.168.8.x:x')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', 'x')  # Required - set this in your environment
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', 'homelab')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', 'ambient-temp-humidity-1min-test')


def read_sensor_data(ser):
    try:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            return None
        temperature, humidity = line.split(',')
        return float(temperature), float(humidity)
    except (ValueError, UnicodeDecodeError) as e:
        print(f"Error parsing line: {line} ({e})")
        return None
def send_data_to_influxdbv2(data):
    try:
        temperature, humidity = data
        timeAtRecord = time.time_ns()
        with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)

            points  = [
                Point("temp").field("value", temperature).time(timeAtRecord),
                Point("humidity").field("value", humidity).time(timeAtRecord)
                       ]

            write_api.write(bucket=INFLUXDB_BUCKET, record=points)
            return True
    except Exception as e:
        print(e)
        return False

def main():
    with serial.Serial(com_port, baud_rate, timeout=1) as ser:
        try:
            while True:
                data = read_sensor_data(ser)
                if data is None:
                    continue
                else:
                    temperature , humidity = data  
                    # print(f"Logged: Temperature={temperature}°C, Humidity={humidity}%")
                    send_data_to_influxdbv2(data)
                time.sleep(60)
        except KeyboardInterrupt:
            print("Data logging stopped.")

if __name__ == '__main__':
    main()