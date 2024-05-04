import time
import smbus
import signal
import sys
import pynmea2
import multiprocessing

BUS = None
address = 0x42
gpsReadInterval = 0.03

# Queue to pass GPS data to main program
gps_queue = multiprocessing.Queue(maxsize=1)  # Max size 1 to keep only the latest data

def connectBus():
    global BUS
    BUS = smbus.SMBus(1)

def parseResponse(gpsLine):
    gpsChars = ''.join(chr(c) for c in gpsLine)
    if gpsChars[0] == '$':
        try:
            msg = pynmea2.parse(gpsChars)
            if isinstance(msg, pynmea2.types.talker.GGA):
                if msg.is_valid:
                    # Clear existing data before putting new data
                    while not gps_queue.empty():
                        _ = gps_queue.get()
                    gps_queue.put({
                        "timestamp": msg.timestamp,
                        "latitude": msg.latitude,
                        "longitude": msg.longitude,
                        "altitude": msg.altitude
                    })
        except pynmea2.ParseError:
            pass  # Ignore parsing errors

def handle_ctrl_c(signal, frame):
    sys.exit(130)

# This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)

def readGPS():
    c = None
    response = []
    try:
        while True:
            c = BUS.read_byte(address)
            if c == 255:
                return False
            elif c == 10:
                break
            else:
                response.append(c)
        parseResponse(bytearray(response))

    except IOError:
        connectBus()
    except Exception as e:
        pass  # Ignore other exceptions

connectBus()

def updateGPSData():
    while True:
        readGPS()
        time.sleep(gpsReadInterval)

def start_reading_process():
    p = multiprocessing.Process(target=updateGPSData)
    p.daemon = True  # Daemon process so it will terminate with the main program
    p.start()

start_reading_process()  # Start the process immediately

