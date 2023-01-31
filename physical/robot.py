from sr.robot3 import *
R = Robot()


R.kch.leds[UserLED.A] = Colour.RED

left_id = 1
mid_id = 2
right_id = 3
    
lit_up = False


while True:
    
    markers = R.camera.see() # markers

    for each in markers:
        if each.id == mid_id:
            R.khc.leds[UserLED.B] = Colour.BLUE # B
            lit_up = True

    if not lit_up:
        for each in markers:
            if each.id == left_id:
                R.khc.leds[UserLED.A] = Colour.BLUE # A
                lit_up = True
            
            elif each.id == right_id:
                R.khc.leds[UserLED.C] = Colour.BLUE # C
        
    
    lit_up = False
    R.sleep(0.1) 
    #motor board srABC1, channel 0 to full power forward
    #R.motor_boards["SR0UDB"].motors[0].power = 1
    #R.motor_boards["SR0UDB"].motors[1].power = 1
