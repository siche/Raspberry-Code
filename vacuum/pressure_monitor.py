import time 
import requests
import math
import random
import serial

# define serial
port = "/dev/ttyUSB0"
ser = serial.Serial(port, 9600, timeout=0.5)

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

# define  token for upload data
TOKEN ="A1E-zCZSSXcfEnEi7qwWV6zv3zWISWye84"
DEVICE_LABEL = "raspi"
VARIABLE_LABEL1 = "pressure"

# Acquire data
def get_data():
    ser.write("#000F\r".encode())
    time.sleep(0.05)
    data = ser.readline()
    data = data[1:-1]
    data = 1e11*float(data)
    data = round(data,3)

    # convert into json
    value = {VARIABLE_LABEL1:data}
    return value

def post_request(payload):
    # the following is the industrial API
    # url = "http://industrial.api.ubidots.com"

    # use free education token
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    # print("[INFO] request made properly, your device is updated")
    return True

def main():

    payload = get_data()

    #print("[INFO] Attemping to send data")
    post_request(payload)
    #print("[INFO] finished")

if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
