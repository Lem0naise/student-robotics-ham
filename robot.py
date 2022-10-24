from sr.robot3 import *
from operator import attrgetter
from random import randrange

R = Robot()


# ---------- MARKER SETUP ----------

ZONE_1_MARKERS = [0, 1, 2, 25, 26, 27]
ZONE_2_MARKERS = [4, 5, 6, 7, 8, 9]
ZONE_3_MARKERS = [11, 12, 13, 14, 15, 16]
ZONE_4_MARKERS = [18, 19, 20, 21, 22, 23]
HOME_MARKERS = ZONE_1_MARKERS # change this when our zone changes
OTHER_MARKERS = [x for x in range(26) if x not in HOME_MARKERS]
TOKEN_MARKERS = [99]
print(OTHER_MARKERS)
old_state = "stationary"
state = "stationary"


# ---------- DEGREE FUNCTION ----------

def rad2deg(rad):
	return rad * 57.2958


# ---------- SPOTTING MARKER ID ----------

def marker(ids): # array
	global state

	cubes = R.camera.see() # make list of all visible cubes
	
	i = 0  # iterator to prevent a 360 degree turn without seeing marker

	if not any(mark.id in ids for mark in cubes): # if no zone markers are found
		return None
	
	else:

		new_cubes = []
		for each in cubes:
			if each.id in ids:
				new_cubes.append(each)

		closest = min(new_cubes, key=attrgetter("distance"))
		return closest



# ---------- SPOTTING MARKER ID ANGLE ----------
def marker_angle(ids):
	mark = marker(ids)
	if mark != None:
		return rad2deg(mark.spherical.rot_y)
	else: return None


# ---------- REFRESHING DISTANCE FUNCTION ----------
def dist_front():
	return R.ruggeduino.pins[A4].analogue_read()


# ---------- SPEED FUNCTION ---------

def speed(speed, motors, stop = False, time = None): # float (-1, 1) ; [array]
	for motor in motors:
		R.motor_board.motors[motor].power = speed
 
	if stop: # if want to stop after a time
		R.sleep(time)
		for motor in motors: # reset back to zero
			R.motor_board.motors[motor].power = 0



# ---------- TURN FUNCTION ---------

TURN_VALUE = 0.005 # the value to change degrees into seconds

def turn(angle):

	if angle > 0: # if turning right
		speed(0.5, [0])
		speed(0, [1])
	else: # if turning left
		speed(0, [0]) 
		speed(0.5, [1])

	R.sleep(TURN_VALUE * abs(angle)) # wait until turned angle

	speed(0, [0, 1]) # stop both


# ~~~~ TODO SMOOTHER MOVING ~~~~
# ~~~~ BETTER AVOIDING OF OBSTACLES (maybe turn instead of reversing) ~~~~


# ---------- MAIN PROGRAM ---------

turn(-80) # very initial turn

while True:
	print(state)

	# -------- SETUP --------
	
	if (state == "stationary"):		
		state = "looking"


	# -------- FINDING TOKEN MARKERS --------

	elif (state == "looking"):

		R.sleep(0.2) # pause before looking
		
		cubes = R.camera.see() # make list of all visible cubes

		if len(cubes) > 0: # if can see any cubes
			closest = marker(TOKEN_MARKERS) # any tokens 
			if closest != None:
				c_dist = closest.distance / 1000

				# -- GETTING ROTATION INFORMATION -- 
				c_angle = rad2deg(closest.spherical.rot_y)
				turn(c_angle)
				R.sleep(0.5)
			
				state = "moving"
			else:
				state = "empty"

		else:

			state = "empty"



	# -------- SEARCHING FOR TOKEN MARKERS ---------
	
	elif (state == "searching for tokens"):
		
		pass


	# -------- SPINNING --------
	elif (state == "empty"):

		speed(-1, [0, 1], True, 0.1)
		c_angle = randrange(60, 100)
		turn(c_angle)
		state = "moving"
		

	# -------- MOVING --------

	elif (state == "moving"):

		speed(1, [0, 1]) # full speed

		if dist_front() < 0.1:            
			speed(0, [0, 1]) # stop

			if marker(TOKEN_MARKERS).distance <= 150: # if about to grab a token and not something else
				state = "grabbing"
			else:
				state = "empty"


	# -------- GRABBING --------

	elif (state == "grabbing"):

		R.servo_board.servos[0].position = 1
		R.servo_board.servos[1].position = 1

		if (dist_front() < 0.3): # if grabbed successfully
			state = "returning"
		else:
			state = "failed grabbing"
	


	# -------- FAILED GRABBING -------- 

	elif (state == "failed grabbing"):

		R.servo_board.servos[0].position = -1
		R.servo_board.servos[1].position = -1
		R.sleep(0.2)
		speed(1, [0, 1], True, 0.2)
		state = "grabbing"



	# -------- RETURNING WITH A TOKEN -------- 

	elif (state == "returning"):

		turn(180)
		h_angle = marker_angle(HOME_MARKERS)
		if h_angle != None: turn(h_angle) # turn the angle of the closest home marker
		speed(1, [0, 1])
		state = "returning moving"
		

	elif (state == "returning moving"):

		speed(1, [0, 1])

		h_marker = marker(HOME_MARKERS)
		if h_marker != None: # if seen a home marker

			if h_marker.distance <= 1000:
				state = "dropping"
				speed(0, [0, 1])

		else: # if cannot see a home marker

			state = "searching for home"



	# -------- SEARCHING FOR HOME ZONE ---------
	
	elif (state == "searching for home"):
		
		while marker(HOME_MARKERS) == None:
			turn(30)
		
		state = "returning moving"



	# -------- DROPPING OFF TOKEN ---------

	elif (state == "dropping"):

		R.servo_board.servos[0].position = -1
		R.servo_board.servos[1].position = -1
		R.sleep(0.2)
		speed(-1, [0, 1], True, 0.2)
		state = "resetting"



	# -------- RESETTING VIEW TO FIND MARKERS NOT IN HOME ZONE ---------

	elif (state == "resetting"):

		o_angle = None

		while o_angle == None: # while cannot yet see another marker
			turn(30)

			o_angle = marker_angle(OTHER_MARKERS)

			R.sleep(0.1)

		state = "stationary"


	# -------- AVOIDING COLLISIONS ---------

	left_dist = R.ruggeduino.pins[A0].analogue_read()
	right_dist = R.ruggeduino.pins[A1].analogue_read()

	if left_dist <= 0.2:
		old_state = state
		state = "avoiding collision left"

	elif right_dist <= 0.2:
		old_state = state
		state = "avoiding collision right"


	if (state == "avoiding collision left"):
		print(state)

		speed(-1, [0, 1], True, 0.5)
		state = old_state

	if (state == "avoiding collision right"):
		print(state)

		speed(-1, [0, 1], True, 0.5)
		state = old_state



	R.sleep(0.2)

