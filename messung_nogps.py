import adafruit_bme680
import time
import board
import mysql.connector
from datetime import datetime
from sensor_reader import *
import threading


# MySQL connection configuration
mysql_config = {
    'user': 'airscout',
    'password': 'sniffer',
    'host': 'localhost',
    'database': 'daten',
}

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data_nogps (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        temperature_bme FLOAT,
        gas INT,
        humidity_bme FLOAT,
        pressure FLOAT,
        altitude FLOAT,
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

def messung():
    while True:
        read_sensor_data()
        timestamp = datetime.now()
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


        print("Timestamp: %s" % timestamp)
        print("\nTemperature: %0.1f C" % temperature_bme)
        print("Gas: %d ohm" % gas)
        print("Humidity: %0.1f %%" % humidity_bme)
        print("Pressure: %0.3f hPa" % pressure)
        print("Altitude = %0.2f meters" % altitude)

        # Insert data into MySQL
        cursor.execute("""
            INSERT INTO sensor_data_nogps (timestamp, temperature_bme, gas, humidity_bme, pressure, altitude, pm_1_0, pm_2_5, pm_10, co2, voc, temperature, humidity, ch2o, co, o3, no2)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (timestamp, temperature_bme, gas, humidity_bme, pressure, altitude, pm_1_0, pm_2_5, pm_10, co2, voc, temperature, humidity, ch2o, co, o3, no2))
        conn.commit()

        time.sleep(5)

#def hellotest():
 #   while True:
  #      print("hello")
   #     time.sleep(2)

t1 = threading.Thread(target=messung)

#t2 = threading.Thread(target=hellotest)

t1.start()
#t2.start()
t1.join()
#t2.join()


# Close connection
conn.close()

