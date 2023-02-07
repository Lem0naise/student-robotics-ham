from sr.robot3 import *
R = Robot()


def task_2():

    left_id = 1
    mid_id = 2
    right_id = 3
        
    lit_up = False
    
    print("set up variables")
    
    while True:
        
        print("loop start")
        markers = R.camera.see() # markers
        print("got markers")

        for each in markers:
            print("finding mid")
            if each.id == mid_id:
                print("found mid")
                R.kch.leds[UserLED.B] = Colour.BLUE # B
                lit_up = True


        if not lit_up:
            print("if can see either of the other markes")
            for each in markers:
                if each.id == left_id:
                    print("saw left marker")
                    R.kch.leds[UserLED.A] = Colour.BLUE # A
                    
                    lit_up = True
                
                elif each.id == right_id:
                    print("saw right marker")
                    R.kch.leds[UserLED.C] = Colour.BLUE # C
            
        
        lit_up = False
            
        R.sleep(0.5) 

        R.kch.leds[UserLED.A] = Colour.OFF
        R.kch.leds[UserLED.B] = Colour.OFF
        R.kch.leds[UserLED.C] = Colour.OFF
        #motor board srABC1, channel 0 to full power forward
        #R.motor_boards["SR0UDB"].motors[0].power = 1
        #R.motor_boards["SR0UDB"].motors[1].power = 1


def task_3():

    mid_id = 2
        
    while True:
            
        markers = R.camera.see()

        for each in markers:
            if each.id == mid_id:

                d = each.distance / 1000
                                
                dist = (abs(d**2 - 1)**0.5) * 1000
                print('HYPOTENUSE', d)
                print('DISTANCE: ', dist)
                print('ANGLE', each.spherical.rot_y)
                if dist <= 200:
                    R.kch.leds[UserLED.B] = Colour.BLUE

                            
                else:
                            
                    if each.spherical.rot_y > 0:
                        R.kch.leds[UserLED.A] = Colour.RED
                    else:
                        R.kch.leds[UserLED.C] = Colour.RED


                break 
            
        
        R.sleep(0.5)

        R.kch.leds[UserLED.A] = Colour.OFF
        R.kch.leds[UserLED.B] = Colour.OFF
        R.kch.leds[UserLED.C] = Colour.OFF

task_3()