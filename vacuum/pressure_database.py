import time 
import requests
import math
import random
import serial
from influxdb import InfluxDBClient
import time

# define serial and connect database
port = "/dev/ttyUSB0"
ser = serial.Serial(port, 9600, timeout=0.5)
db_client = InfluxDBClient('192.168.1.13',8086,database='mingming')

# serial properities
ser.bytesize = serial.EIGHTBITS # Number of data bits
ser.parity = serial.PARITY_NONE # Enable parity checking
ser.stopbits = serial.STOPBITS_ONE #Number of stop bits
ser.xonxoff = False #Software flow control     
ser.rtscts = False # Hardware flow control (RTS/CTS)   
ser.dsrdtr = False  # Hardware flow control (DSR/DTR)

# Open serial
if not ser.isOpen():
    try:
        ser.open()
    except Exception as e:
        print("something is wrong with serail")
        print(e)
        exit()

ser.flushInput()
ser.flushOutput()

# Acquire data
def get_data():
    ser.write("#000F\r".encode())
    time.sleep(0.05)
    data = ser.readline()
    data = data[1:-1]
    # print(data)
    # data = 1e11*float(data)
    return float(data)

def send_data():
    while True:
        data = get_data()
        json_data = [
            {
                "measurement":"mingming-pressure",
                "tags":{
                    "location":"s208"
                },
                "fields":{
                    "pressure":data
                }
            }
        ]
        db_client.write_points(json_data)
            # print('writinng')
        time.sleep(4)

if __name__ == "__main__":
    send_data()
