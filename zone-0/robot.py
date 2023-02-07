from sr.robot3 import *
from operator import attrgetter
from random import randrange
import numpy as np

R = Robot()

# ---------- MARKER SETUP ----------

ZONE_1_MARKERS = [25, 26, 27, 0, 1, 2]
ZONE_2_MARKERS = [4, 5, 6, 7, 8, 9]
ZONE_3_MARKERS = [11, 12, 13, 14, 15, 16]
ZONE_4_MARKERS = [18, 19, 20, 21, 22, 23]
ZONE_TO_MARKER = {
	0: ZONE_1_MARKERS,
	1: ZONE_2_MARKERS,
	2: ZONE_3_MARKERS,
	3: ZONE_4_MARKERS,
	}

WALL_1 = [x for x in range(7)];
WALL_2 = [x for x in range(7, 14)];
WALL_3 = [x for x in range(14, 21)];
WALL_4 = [x for x in range(21, 28)];

HOME_MARKERS = ZONE_TO_MARKER[R.zone] # Automatically change R.zone when our zone changes in the competition

print(R.zone, HOME_MARKERS)

# set OTHER_MARKERS to all wall markers other than [home markers and centre markers]
OTHER_MARKERS = [x for x in range(26) if (x not in HOME_MARKERS) and (x not in [3, 10, 17, 24])]

# all token markers have id of 99
TOKEN_MARKERS = [99]


# ---------- DEGREE AND RADIAN FUNCTIONS ----------

def d2r(degrees):
    """
    convert from degrees to radians
    return: radians
    """
    return degrees * (np.pi / 180)

def rad2deg(rad):
    """
    convert from radians to degrees
    return: degrees
    """
    return rad * (180 / np.pi)

#def rad2deg(rad):
	#return rad * 57.2958


# ---------- SPOTTING MARKER ID ----------

def marker(ids): # array

	cubes = R.camera.see() # make list of all visible cubes
	
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

def speed(speed, motors, stop = False, time = None): # speed: float(-1, 1) ; motors: [array]

	for motor in motors:
		R.motor_board.motors[motor].power = speed
 
	if stop: # if want to stop after a time
		R.sleep(time)
		for motor in motors: # reset back to zero
			R.motor_board.motors[motor].power = 0



# ---------- TURN FUNCTION ---------

TURN_VALUE = 0.005 # the value to change degrees into seconds

def turn(angle):

	if angle > 0: # turning right
		speed(0.5, [0]) 
		speed(0, [1]) 
	else: # turning left
		speed(0, [0]) 
		speed(0.5, [1])

	R.sleep(TURN_VALUE * abs(angle)) # wait until turned angle

	speed(0, [0, 1]) # stop both



# ~~~~ TODO SMOOTHER MOVING ~~~~
# ~~~~ BETTER AVOIDING OF OBSTACLES  ~~~~
# ~~~~ DONT AVOIDING WHEN GRABBING  ~~~~
# ~~~~ DONT GET STUCK ON STICKY OUT THINGS WHEN LEFT AND RIGHT CANNOT SEE ~~~~
# ~~~~ IF GETS STUCK IN CORNER, CANNOT SEE HOME MARKERS ~~~~


# ---------- MAIN PROGRAM ---------
state = "stationary"

# open the grabbers
R.servo_board.servos[0].position = -1
R.servo_board.servos[1].position = -1

turn(-120) # very initial turn

while True:
	
	print(state) # logging state to console

	# -------- SETUP --------
	# -------- SETTING VIEW TO FIND MARKERS NOT IN HOME ZONE ---------
	if (state == "stationary"):		

		o_angle = None

		while o_angle == None: # while cannot yet see another marker
			turn(30)
			o_angle = marker_angle(OTHER_MARKERS)
			R.sleep(0.1)

		state = "looking"


	# -------- FINDING TOKEN MARKERS --------

	elif (state == "looking"):

		R.sleep(0.05) # pause before looking
		
		cubes = R.camera.see() # make list of all visible cubes

		if len(cubes) > 0: # if can see any cubes
			closest = marker(TOKEN_MARKERS) # closest token marker object
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
		c_angle = randrange(60, 100) # turn random degrees to right
		turn(c_angle)
		state = "looking" # set back to looking for markers
		

	# -------- MOVING TO MARKER --------

	elif (state == "moving"):

		speed(1, [0, 1]) # full speed

		m_angle = marker_angle(TOKEN_MARKERS) # check angle to the closest marker
		
		if m_angle == None: # if for some reason have completely lost sight of marker
			state = "looking" # reset to looking
			
		else:
			if m_angle >= 10 or m_angle <= -10: # if the angle of deviation is enough to care about
				turn(m_angle)
			

			if dist_front() < 0.1: # if about to hit it     
				speed(0, [0, 1]) # stop


				closest_marker = marker(TOKEN_MARKERS)
				if closest_marker:
					if closest_marker.distance <= 400: # if about to grab a token and not a wall or other bot
						state = "grabbing"
					else:
						state = "empty"



	# -------- GRABBING --------

	elif (state == "grabbing"):
		
		R.servo_board.servos[0].position = 1
		R.servo_board.servos[1].position = 1

		if (dist_front() < 0.3): # if grabbed successfully
			state = "finding home"
		else:
			state = "failed grabbing"
	


	# -------- FAILED GRABBING -------- 

	elif (state == "failed grabbing"):

		# release
		R.servo_board.servos[0].position = -1
		R.servo_board.servos[1].position = -1

		R.sleep(0.2) # sleep for 0.2 seconds
		speed(1, [0, 1], True, 0.2) # ram into box again	
		state = "grabbing" # try to grab again



	# -------- FINDING HOME TO RETURN TO  -------- 

	elif (state == "finding home"):

		h_angle = marker_angle(HOME_MARKERS) # find home marker
		total_turned = 0

		# continue spinning while you cannot see any home markers 
		# if have turned a full circle, stop the loop
		while (h_angle == None) and (total_turned < 360):

			h_angle = marker_angle(HOME_MARKERS) # see if a home marker appears

			turn(15)
			total_turned += 15


		if h_angle != None: # if we found a home marker
			turn(h_angle) # turn the angle of the closest home marker

			state = "returning"

		elif total_turned >= 360: # if instead we turned a full circle
			pass	


	# -------- RETURNING BACK TO HOME WITH A TOKEN ---------
	elif (state == "returning"):

		speed(1, [0, 1])

		h_marker = marker(HOME_MARKERS)
		if h_marker != None: # if seen a home marker

			if h_marker.distance <= 2500: # if the closest home marker is less than 2.5m away
				state = "dropping" # set state to dropping
				speed(0, [0, 1])

		else: # if cannot see a home marker

			state = "finding home"



	# -------- DROPPING OFF TOKEN ---------

	elif (state == "dropping"):

		# release 
		R.servo_board.servos[0].position = -1
		R.servo_board.servos[1].position = -1

		R.sleep(0.2)
		speed(-1, [0, 1], True, 0.2) # reverse
		state = "stationary" # reset to looking for markers



	# -------- AVOIDING COLLISIONS ---------

	left_dist = R.ruggeduino.pins[A0].analogue_read()
	right_dist = R.ruggeduino.pins[A1].analogue_read()

	if left_dist <= 0.2:
		old_state = state

		if state not in ["grabbing", "failed grabbing"]: # don't avoid if grabbing
			state = "avoiding collision left"

	elif right_dist <= 0.2:
		old_state = state
		
		if state not in ["grabbing", "failed grabbing"]: # don't avoid if grabbing
			state = "avoiding collision right"


	if (state == "avoiding collision left"):
		print(state)

		speed(-1, [0, 1], True, 0.2) # reverse for 0.2s
		speed(1, [0], True, 0.3) # turn right for 0.3s
		state = old_state

	if (state == "avoiding collision right"):
		print(state)

		speed(-1, [0, 1], True, 0.2)  # reverse for 0.2s
		speed(1, [1], True, 0.3)  # turn left for 0.3s
		state = old_state

	R.sleep(0.2)

