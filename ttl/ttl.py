import RPi.GPIO as GPIO
import sys
import time

LED = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)


class ttl(object):
    def __init__(self):
        self.LED = 21
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED,GPIO.OUT)
        self.gpio = GPIO

    def on(self):
        self.gpio.output(self.LED,True)
    
    def off(self):
        self.gpio.output(self.LED,False)
    
if __name__ == '__main__':
    ttl = ttl()
    ttl.on()
