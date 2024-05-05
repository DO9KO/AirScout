#!/usr/bin/env python3


import threading
import queue
import adafruit_bme680
import time
import board
import mysql.connector
from datetime import datetime
from sensor_reader import *
import Display
import pytz
import gps_reader


# MySQL connection configuration
mysql_config = {
    'user': 'airscout',
    'password': 'sniffer24',
    'host': 'localhost',
    'database': 'daten',
}

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        temperature_bme FLOAT,
        gas INT,
        humidity_bme FLOAT,
        pressure FLOAT,
        altitude FLOAT,
        latitude DOUBLE,
        longitude DOUBLE,
        pm_1_0 INT,
        pm_2_5 INT,
        pm_10 INT,
        co2 INT,
        voc INT,
        temperature FLOAT,
        humidity INT,
        ch2o FLOAT,
        co FLOAT,
        o3 FLOAT,
        no2 FLOAT
    )
""")
conn.commit()

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# Queue for sharing data between threads
data_queue = queue.Queue(maxsize=1)  # Only store the latest data

def messung():
    while True:
        gps_data = gps_reader.gps_queue.get()
        latitude = gps_data["latitude"]
        longitude = gps_data["longitude"]
        altitude_gps = gps_data["altitude"]
        timestamp_gps = gps_data["timestamp"]
        timestamp = datetime.now()
        read_sensor_data()
        temperature_bme = bme680.temperature
        gas = bme680.gas
        humidity_bme = bme680.relative_humidity
        pressure = bme680.pressure
        altitude = bme680.altitude
        pm_1_0 = get_pm_1_0()
        pm_2_5 = get_pm_2_5()
        pm_10 = get_pm_10()
        co2 = get_co2()
        voc = get_voc()
        temperature = get_temperature()
        humidity = get_humidity()
        ch2o = get_ch2o()
        co = get_co()
        o3 = get_o3()
        no2 = get_no2()
        uhr = datetime.now(pytz.utc).astimezone(pytz.timezone('Europe/Berlin')).strftime("%H:%M Uhr")
        
        # Remove previous data from the queue
        while not data_queue.empty():
            data_queue.get()

        # Put new data into the queue
        data_queue.put((uhr, temperature_bme, gas, humidity_bme, pressure, altitude, pm_1_0, pm_2_5, pm_10, co2, voc, temperature, humidity, ch2o, co, o3, no2))

        # Insert data into MySQL
        cursor.execute("""
        INSERT INTO sensor_data (timestamp, temperature_bme, gas, humidity_bme, pressure, altitude, latitude, longitude, pm_1_0, pm_2_5, pm_10, co2, voc, temperature, humidity, ch2o, co, o3, no2)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (timestamp, temperature_bme, gas, humidity_bme, pressure, altitude, latitude, longitude, pm_1_0, pm_2_5, pm_10, co2, voc, temperature, humidity, ch2o, co, o3, no2))
        conn.commit()
        time.sleep(5)

# Funktion, die auf die Variablen der ersten Funktion zugreift
def display():
    while True:
        # Get data from the queue
        data = data_queue.get()

        # Unpack data
        timestamp, temperature_bme, gas, humidity_bme, pressure, altitude, pm_1_0, pm_2_5, pm_10, co2, voc, temperature, humidity, ch2o, co, o3, no2 = data

        # Display data
        Display.Programm(pm_1_0, pm_2_5, pm_10, co2, co, o3, no2, temperature, humidity, timestamp)
        
        time.sleep(20)

# Messungsfunktion in einem Thread ausführen
t1 = threading.Thread(target=messung)
t1.start()

# Anzeigefunktion in einem separaten Thread ausführen
t2 = threading.Thread(target=display)
t2.start()

# Auf beide Threads warten, bevor das Programm endet
t1.join()
t2.join()


# Close connection
conn.close()

