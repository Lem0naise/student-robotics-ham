
# 02 July 2022
# # Base I2c (8 bit) address for the MD25 (Orange box) is xB2
# NB MD25 MUST BE CONNECTED TO Odroid USB port directly NOT VIA USB HUB
# Ruggedino flashed with Basic firmware. NB use new arduino bootloader?
# Motor board SR0NFC
# Motor board SR0TH1Q
# Ruggeduino - 75230313833351617141
# Servo Board - sr0HG37



#import usb
#import pyudev   # ignore import error
from sr.robot3 import * # New SR code based on Python 3.9

import time

R = Robot()

while True:
    for pin in range(6,12):       
        R.ruggeduino.pins[pin].mode = OUTPUT
    for pin in range(6,12):
        print("LED pin ",pin) 
        R.ruggeduino.pins[pin].digital_write(True) 
        time.sleep(1)
        R.ruggeduino.pins[pin].digital_write(False) 
        time.sleep(1) 

