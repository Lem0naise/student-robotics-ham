from sr.robot3 import *
from operator import attrgetter
R = Robot()

id_to_board = {
	0: "SR0UDB",
	1: "SR0VG1M"
}
TOKEN_MARKERS = [73]

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

# Use R.zone instead
HOME_MARKERS = ZONE_TO_MARKER[1] # Automatically change R.zone when our zone changes in the competition
print(1, HOME_MARKERS)


#R.motor_boards["SR0VG1M"].motors[0] BACK RIGHT WHEEL
#R.motor_boards["SR0VG1M"].motors[1] FRONT RIGHT WHEEL
#R.motor_boards["SR0UDB"].motors[0] BACK LEFT WHEEL
#R.motor_boards["SR0UDB"].motors[1] FRONT LEFT WHEEL


# ---------- SPEED FUNCTION ---------

def speed(speed, motors, stop = False, time = None): # speed: float(-1, 1) ; motors: [array]

	for motor in motors:
		R.motor_boards[id_to_board[motor]].motors[0].power = speed
		R.motor_boards[id_to_board[motor]].motors[1].power = speed
 
	if stop: # if want to stop after a time
		R.sleep(time)
		for motor in motors: # reset back to zero
			R.motor_boards[id_to_board[motor]].motors[motor].power = 0

# ---------- RADIANS TO DEGREES ---------
def rad2deg(rad):
	return rad * (180 / 3.14159)


# ---------- TURN FUNCTION ---------
TURN_VALUE = 0.0244 # the value to change degrees into seconds

def turn(angle):
	global bearing
	if angle > 0: # turning right
		speed(0.15, [0]) 
		speed(-0.15, [1]) 
	else: # turning left
		speed(-0.15, [0]) 
		speed(0.15, [1])

	R.sleep(TURN_VALUE * abs(angle)) # wait until turned angle
	#print('PREV BEARING:', bearing)
	#bearing = (bearing - angle) % 360
	#print('NEW BEARING:', bearing)
	print('turn', angle)
	speed(0, [0, 1]) # stop both


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
			markers = cubes
			print(markers)
			for m in markers:
				print()
				print(m.distance)
	
				if m.id == 73 and m.distance > 0 and closest == None: # if is a token, and 50cm away, and not already a closest
					closest = m

			if closest != None:

				c_dist = closest.distance / 1000

				# -- GETTING ROTATION INFORMATION -- 
				c_angle = rad2deg(closest.spherical.rot_y)
				turn(c_angle)
				R.sleep(0.1)
				old_distance = closest.distance
				state = "moving"
				iterator = 0
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
	
	

	# -------- GOING TO TOKEN --------

	elif (state == "moving"):
		
		speed(0.4, [0, 1]) # full speed

		token = marker(TOKEN_MARKERS)
		# checking whether have hit it
		closest = token
		if (closest == None) or (closest.distance > old_distance+30): # if the new closest marker is further away (plus 30mm)
			print("Hit token")
			speed(0.4, [0, 1], True, 0.5) # full speed
			speed(0, [0, 1]) # stop
			R.sleep(0.5)
			turn(-100)
			R.sleep(0.2)
			while marker(HOME_MARKERS) == None:
				turn(-30)
				R.sleep(0.5) # wait for 0.5 seconds to take a picture
			state = "going home"
	

		else:
			
			m_angle = rad2deg(token.spherical.rot_y) # check angle to the closest marker
			if m_angle == None: # if for some reason have completely lost sight of marker
				state = "looking" # reset to looking
			else:
				print(abs(m_angle))
				if abs(m_angle) > 5: # if the angle of deviation is enough to care about
					turn(m_angle-2)
		

			old_distance = closest.distance

	# -------- GOING TO MARKER --------
	
	elif (state == "going home"):

		speed(0.1, [0, 1]) # head towards the home marker (slowly for testing)
		m_home = marker(HOME_MARKERS)
		if m_home == None: # once can no longer see home
			state = "dropping"
		else:
			m_angle = rad2deg(m_home.spherical.rot_y)
			if abs(m_angle) > 10:
				turn(m_angle)

			if m_home.distance < 200:
				speed(0, [0, 1])
				state = "dropping"

	elif (state == "dropping"):
		speed(-0.5, [0, 1], True, 1) # reverse for 1 second
		state = "home"

	elif (state == "home"):
		speed(0, [0, 1])

	R.sleep(0.2)