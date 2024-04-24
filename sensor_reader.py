import serial
import time
from datetime import datetime

# Serial connection initialization
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.1)

# Function to read sensor data
def read_sensor_data():
    command = bytes([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    uart.write(command)
    time.sleep(0.1)
    response = uart.read(26)
    if response and len(response) == 26:
        if response[0] == 0xFF and response[1] == 0x86:
            checksum = (256 - sum(response[0:23]) % 256) - 1
            if checksum == response[25]:
                pm_1_0 = response[2] * 256 + response[3]
                pm_2_5 = response[4] * 256 + response[5]
                pm_10 = response[6] * 256 + response[7]
                co2 = response[8] * 256 + response[9]
                voc = response[10]
                temperature = ((response[11] * 256 + response[12]) - 400) * 0.1
                humidity = response[13] * 256 + response[14]
                ch2o = (response[15] * 256 + response[16]) * 0.001
                co = (response[17] * 256 + response[18]) * 0.1
                o3 = (response[19] * 256 + response[20]) * 0.01
                no2 = (response[21] * 256 + response[22]) * 0.01

                return {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "PM1.0": pm_1_0,
                    "PM2.5": pm_2_5,
                    "PM10": pm_10,
                    "CO2": co2,
                    "VOC": voc,
                    "Temperature": temperature,
                    "Humidity": humidity,
                    "CH2O": ch2o,
                    "CO": co,
                    "O3": o3,
                    "NO2": no2
                }
            else:
                print("Invalid response (checksum error)!")
        else:
            print("Invalid response (wrong command)!")
            time.sleep(5)
    else:
        print("No valid response received!")
        time.sleep(2)

# Functions to get sensor values
def get_pm_1_0():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("PM1.0")

def get_pm_2_5():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("PM2.5")

def get_pm_10():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("PM10")

def get_co2():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("CO2")

def get_voc():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("VOC")

def get_temperature():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("Temperature")

def get_humidity():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("Humidity")

def get_ch2o():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("CH2O")

def get_co():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("CO")

def get_o3():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("O3")

def get_no2():
    sensor_data = read_sensor_data()
    if sensor_data:
        return sensor_data.get("NO2")

