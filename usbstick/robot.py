from sr.robot3 import *
R = Robot()


#R.motor_boards["SR0VG1M"].motors[0] BACK RIGHT WHEEL
#R.motor_boards["SR0VG1M"].motors[1] FRONT RIGHT WHEEL
#R.motor_boards["SR0UDB"].motors[0] BACK LEFT WHEEL
#R.motor_boards["SR0UDB"].motors[1] FRONT LEFT WHEEL


# ---------- SPEED FUNCTION ---------

def speed(speed, motors, stop = False, time = None): # speed: float(-1, 1) ; motors: [array]

	for motor in motors:
		R.motor_boards["SR0VG1M"].motors[motor].power = speed
 
	if stop: # if want to stop after a time
		R.sleep(time)
		for motor in motors: # reset back to zero
			R.motor_boards["SR0VG1M"].motors[motor].power = 0

# ---------- RADIANS TO DEGREES ---------
def rad2deg(rad):
    return rad * (180 / 3.14159)


# ---------- TURN FUNCTION ---------
TURN_VALUE = 0.005 # the value to change degrees into seconds

def turn(angle):
	global bearing
	if angle > 0: # turning right
		speed(0.5, [0]) 
		speed(0, [1]) 
	else: # turning left
		speed(0, [0]) 
		speed(0.5, [1])

	R.sleep(TURN_VALUE * abs(angle)) # wait until turned angle
	#print('PREV BEARING:', bearing)
	#bearing = (bearing - angle) % 360
	#print('NEW BEARING:', bearing)
	print('turn', angle)
	speed(0, [0, 1]) # stop both



state = "stationary"

while True:
	
	print(state)
	old_state = state

	if state == "stationary":
		state = "looking"


	# -------- FINDING TOKEN MARKERS --------

	elif (state == "looking"):

		R.sleep(0.05) # pause before looking
		
		cubes = R.camera.see() # make list of all visible cubes

		if len(cubes) > 0: # if can see any cubes
			closest = None
			markers = R.camera.see() 
			print(markers)
			for m in markers:
				if m.id == 73 and m.distance > 1500 and closest == None:
					closest = m
			if closest != None:
				c_dist = closest.distance / 1000

				# -- GETTING ROTATION INFORMATION -- 
				c_angle = rad2deg(closest.spherical.rot_y)
				turn(c_angle)
				R.sleep(0.1)
			
				state = "moving"
			else:
				state = "empty"

		else:

			state = "empty"


	# -------- SPINNING IF CANNOT SEE ANY MARKERS --------

	elif (state == "empty"):

		speed(-1, [0, 1], True, 0.1) # reverse for 0.1 seconds
		c_angle = 70 # turn 70 (random) degrees to right
		turn(c_angle)
		state = "looking" # set back to looking for markers
	
	
	R.sleep(0.2)