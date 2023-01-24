from sr.robot3 import *

#import time
from sr.robot3 import *
R = Robot()
print("Hello worldssss")
#while True:
R.kch.leds[UserLED.A] = Colour.RED
    #R.kch.leds[UserLED.A] = Colour.OFF
    #R.kch.leds[UserLED.A] = Colour.BLUE
    
while True:
    #motor board srABC1, channel 0 to full power forward
    print("about to the motor i thin")

    R.motor_boards["SR0UDB"].motors[0].power = 1
    R.motor_boards["SR0UDB"].motors[1].power = 1
    print("done the motor")


    # motor board srABC1, channel 1 to half power forward
        #R.motor_boards["SR0UDB"].motors[1].power = -0.2
        
        #R.servo_board.servos[0].position = 0.2