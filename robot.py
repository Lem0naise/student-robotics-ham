from sr.robot3 import *

R = Robot()

distance = R.ruggeduino.pins[A5].analogue_read()
print(f"Rear ultrasound distance: {distance} meters")



# first motor board, both channels to half power forward
R.motor_board.motors[0].power = 0
R.motor_board.motors[1].power = 0.5
R.sleep(0.6)
# sleep for 3 second

R.motor_board.motors[0].power = 0.5
R.motor_board.motors[1].power = 0.5
R.sleep(2)

# first motor board, both channels to stop
R.motor_board.motors[0].power = 0
R.motor_board.motors[1].power = 0

print("Finished moving")
# sleep for 2 second
R.sleep(2)

print("finished resting")
# servos to grab
print("starting servo")
R.servo_board.servos[0].position = 1
R.servo_board.servos[1].position = 1



# sleep for 2 second
R.sleep(2)
print("finished servo")

R.motor_board.motors[0].power = 1
R.motor_board.motors[1].power = 0

R.sleep(0.7)

R.motor_board.motors[0].power = 1
R.motor_board.motors[1].power = 1

R.sleep(3)