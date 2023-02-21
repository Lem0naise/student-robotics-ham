from sr.robot3 import *
from operator import attrgetter
from random import randrange
import math

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

HOME_MARKERS = ZONE_TO_MARKER[R.zone] # R.zone automatically changes when our zone changes

print(R.zone, HOME_MARKERS)

# set OTHER_MARKERS to all wall markers other than [home markers and centre markers]
OTHER_MARKERS = [x for x in range(26) if (x not in HOME_MARKERS) and (x not in [3, 10, 17, 24])]

# all token markers have id of 99
TOKEN_MARKERS = [99]

ARENA_SIDE_LENGTH = 5750

DIST_BETWEEN_ZONE_MARKERS = 718

bearing = (90 + 90 * R.zone) % 360


# ---------- DEGREE FUNCTION ----------

def rad2deg(rad):
	return rad * 57.2958


# ---------- DEGREE FUNCTION ----------

def m2mm(m):
	return m * 1000


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

	global bearing

	if angle > 0: # if turning right
		speed(0.5, [0])
		speed(0, [1])
	else: # if turning left
		speed(0, [0]) 
		speed(0.5, [1])

	R.sleep(TURN_VALUE * abs(angle)) # wait until turned angle
	bearing = (bearing+angle)%360
	speed(0, [0, 1]) # stop both


	
# ---------- POSITION FINDING FUNCTION ---------
def Biangulate(each):
	print(each)
	global bearing
	northcorrection = bearing
	wallno = each.id // 7
	distance = each.distance
	angle = math.radians(math.degrees(each.spherical.rot_y) + bearing)
	x_total = 0
	y_total = 0
	if each.spherical.rot_y < 0:
		angle = math.radians(math.degrees(-1 * each.spherical.rot_y) + bearing)

	if wallno == 0:
		#print(each.id)
			#print('POSITIVE ANGLE')
			#print(distance, angle, math.sin(angle))
		x_distance = - 1 * distance * math.sin(angle) + DIST_BETWEEN_ZONE_MARKERS * (each.id + 1)
		y_distance = distance * math.cos(abs(angle))

	elif wallno == 1:

		y_distance = -1 * distance * math.sin(angle) + DIST_BETWEEN_ZONE_MARKERS * (each.id - 6)
		x_distance = ARENA_SIDE_LENGTH - distance * math.cos(abs(angle))
	
	elif wallno == 2:
		x_distance = ARENA_SIDE_LENGTH - distance * math.sin(angle) - DIST_BETWEEN_ZONE_MARKERS * (each.id - 13)
		y_distance = ARENA_SIDE_LENGTH - distance * math.cos(abs(angle))

	elif wallno == 3:
		y_distance = ARENA_SIDE_LENGTH - distance * math.sin(angle) - DIST_BETWEEN_ZONE_MARKERS * (each.id - 20)
		x_distance = distance * math.cos(abs(angle))
	
	if x_distance < 0:
		x_distance *= -1
	if y_distance < 0:
		y_distance *= -1



def Triangulate():

	cubes = R.camera.see() # make list of all visible cubes
	
	if len(cubes) == 0: # if no zone markers are found
		return None
	
	else:

		new_cubes = []
		for each in cubes:
			if each.id in range(0, 27):
				new_cubes.append(each)
		if len(new_cubes) == 0:
			return None
		elif len(new_cubes) == 1:
			print(Biangulate(new_cubes[-1]))
		wall0 = []
		wall1 = []
		wall2 = []
		wall3 = []
		for each in new_cubes:
			if each.id//7==0:
				wall0.append(each)
			elif each.id//7==1:
				wall1.append(each)
			elif each.id//7==2:
				wall2.append(each)
			elif each.id//7==3:
				wall3.append(each)
		if len(wall0)>1:
			marker1 = wall0[0]
			marker2 = wall0[1]
		elif len(wall1)>1:
			marker1 = wall1[0]
			marker2 = wall1[1]
		elif len(wall2)>1:
			marker1 = wall2[0]
			marker2 = wall2[1]
		elif len(wall3)>1:
			marker1 = wall3[0]
			marker2 = wall3[1]
		else:
			return None
		
		if not any(new_cubes): # if no zone markers are found
			return None
		
		markerlist = [[(i+1)*DIST_BETWEEN_ZONE_MARKERS,0] for i in range(7)]
		for i in range(7):
			markvec = [ARENA_SIDE_LENGTH,(i+1)*DIST_BETWEEN_ZONE_MARKERS]
			markerlist.append(markvec)
		for i in range(7):
			markvec = [ARENA_SIDE_LENGTH-((i+1)*DIST_BETWEEN_ZONE_MARKERS),ARENA_SIDE_LENGTH]
			markerlist.append(markvec)
		for i in range(7):
			markvec = [0,ARENA_SIDE_LENGTH-((i+1)*DIST_BETWEEN_ZONE_MARKERS)]
			markerlist.append(markvec)		

		dist1 = marker1.distance
		dist2 = marker2.distance
		id1 = marker1.id
		id2 = marker2.id
		vector1 = markerlist[id1]
		vector2 = markerlist[id2]
		markdist = abs((vector1[0]-vector2[0])+(vector1[1]-vector2[1]))
		s = (dist1+dist2+markdist)/2
		area = (s*(s-dist1)*(s-dist2)*(s-markdist))**0.5
		
		perpdist = area/(0.5*markdist)
		wallno = id1//7

		if wallno%2==0:
			if wallno==0:
				y = perpdist
			else:
				y = ARENA_SIDE_LENGTH - perpdist
			x1 = vector1[0]
			x2 = vector2[0]
			xdist1a = (dist1**2 - perpdist**2)**0.5
			xdist1b = -xdist1a
			xdist2a = (dist2**2 - perpdist**2)**0.5
			xdist2b = -xdist2a
			poss0 = abs((x1+xdist1a)-(x2+xdist2a))
			poss1 = abs((x1+xdist1b)-(x2+xdist2a))
			poss2 = abs((x1+xdist1a)-(x2+xdist2b))
			poss3 = abs((x1+xdist1b)-(x2+xdist2b))
			posslist = [poss0,poss1,poss2,poss3]
			minposs = posslist.index(min(posslist))
			if poss0 < poss1 and poss0 < poss2 and poss0 < poss3:
				x = ((x1+xdist1a)+(x2+xdist2a))/2
			elif poss1 < poss0 and poss1 < poss2 and poss1 < poss3:
				x = ((x1+xdist1b)+(x2+xdist2a))/2
			elif poss2 < poss0 and poss2 < poss1 and poss2 < poss3:
				x = ((x1+xdist1a)+(x2+xdist2b))/2
			elif poss3 < poss0 and poss3 < poss2 and poss3 < poss1:
				x = ((x1+xdist1b)+(x2+xdist2b))/2
			return [x,y]

		else:
			if wallno==1:
				x = ARENA_SIDE_LENGTH - perpdist
			else:
				x = perpdist
			y1 = vector1[1]
			y2 = vector2[1]
			ydist1a = (dist1**2 - perpdist**2)**0.5
			ydist1b = -ydist1a
			ydist2a = (dist2**2 - perpdist**2)**0.5
			ydist2b = -ydist2a
			poss0 = abs((y1+ydist1a)-(y2+ydist2a))
			poss1 = abs((y1+ydist1b)-(y2+ydist2a))
			poss2 = abs((y1+ydist1a)-(y2+ydist2b))
			poss3 = abs((y1+ydist1b)-(y2+ydist2b))
			posslist = [poss0,poss1,poss2,poss3]
			minposs = posslist.index(min(posslist))
			if minposs==0:
				y = ((y1+ydist1a)+(y2+ydist2a))/2
			elif minposs==1:
				y = ((y1+ydist1b)+(y2+ydist2a))/2
			elif minposs==2:
				y = ((y1+ydist1a)+(y2+ydist2b))/2
			elif minposs==3:
				y = ((y1+ydist1b)+(y2+ydist2b))/2
			return [x,y]


		#Origin is in the top-left hand corner
		'''x_total = 0
		y_total = 0
		for each in new_cubes:
			x_distance = 0
			distance = each.distance
			angle = each.spherical.rot_y

			if each.id in range(0, 7):
				#print(each.id)
				if angle < 0:
					#print('NEGATIVE ANGLE')
					x_distance = distance * math.sin(- 1 * angle) + DIST_BETWEEN_ZONE_MARKERS * (each.id + 1)
				else:
					#print('POSITIVE ANGLE')
					#print(distance, angle, math.sin(angle))
					x_distance = - 1 * distance * math.sin(angle) + DIST_BETWEEN_ZONE_MARKERS * (each.id + 1)
				y_distance = distance * math.cos(abs(angle))

			elif each.id in ZONE_2_MARKERS:
				if angle < 0:
					y_distance = m2mm(distance * math.sin(- 1 * angle)) + DIST_BETWEEN_ZONE_MARKERS * (each.id - 6)
				else:
					y_distance = - 1 * m2mm(distance * math.sin(angle)) + DIST_BETWEEN_ZONE_MARKERS * (each.id - 6)
				x_distance = ARENA_SIDE_LENGTH - m2mm(distance * math.cos(abs(angle)))
			
			elif each.id in ZONE_3_MARKERS:
				if angle < 0:
					x_distance = ARENA_SIDE_LENGTH + m2mm(distance * math.sin(- 1 * angle)) - DIST_BETWEEN_ZONE_MARKERS * (each.id - 13)
				else:
					x_distance = ARENA_SIDE_LENGTH - m2mm(distance * math.sin(angle)) - DIST_BETWEEN_ZONE_MARKERS * (each.id - 13)
				y_distance = ARENA_SIDE_LENGTH - m2mm(distance * math.cos(abs(angle)))

			elif each.id in ZONE_4_MARKERS:
				if angle < 0:
					y_distance = ARENA_SIDE_LENGTH + m2mm(distance * math.sin(- 1 * angle)) - DIST_BETWEEN_ZONE_MARKERS * (each.id - 20)
				else:
					y_distance = ARENA_SIDE_LENGTH - m2mm(distance * math.sin(angle)) - DIST_BETWEEN_ZONE_MARKERS * (each.id - 20)
				x_distance = m2mm(distance * math.cos(abs(angle)))
			x_total += x_distance
			y_total += y_distance
			print(x_distance, 'test')

		x_average = x_total / len(new_cubes)
		y_average = y_total / len(new_cubes)
		return (x_average, y_average)'''


def Navigate(x2, y2):
	global bearing
	x1 = Triangulate()[0]
	y1 = Triangulate()[1]
	if x2==x1:
		direction = 0
	else:
		m = (y2-y1)/(x2-x1)
		angle = math.degrees(math.atan(m))
		if angle<0:
			angle += 180
		if m == 0:
			direction = 90
		elif m>0 and x2>x1:
			direction = 90-angle
		elif m>0 and x2<x1:
			direction = 270-angle
		elif m<0 and x2<x1:
			direction = angle-90
		elif m<0 and x2>x1:
			direction = angle+90
	turn(direction-bearing)
	speed(1, [0, 1]) # full speed


	

			
		

	
	



# ~~~~ TODO SMOOTHER MOVING ~~~~
# ~~~~ BETTER AVOIDING OF OBSTACLES  ~~~~
# ~~~~ DONT AVOIDING WHEN GRABBING  ~~~~
# ~~~~ DONT GET STUCK ON STICKY OUT THINGS WHEN LEFT AND RIGHT CANNOT SEE ~~~~
# ~~~~ IF GETS STUCK IN CORNER, CANNOT SEE HOME MARKERS ~~~~


# ---------- MAIN PROGRAM ---------
turn(-120) # very initial turn
state = 'stationary'
while True:
	
	print(state) # logging state to console
	#Triangulate()

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
		print(Triangulate())
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

				if marker(TOKEN_MARKERS).distance <= 150: # if about to grab a token and not a wall or other bot
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
			
			current_coords = Triangulate()
			if current_coords != None:
				CUTOFF = ARENA_SIDE_LENGTH / 2
				if current_coords[0] < CUTOFF and current_coords[1] < CUTOFF:
					zone = 1
				if current_coords[0] > CUTOFF and current_coords[1] < CUTOFF:
					zone = 2
				if current_coords[0] > CUTOFF and current_coords[1] > CUTOFF:
					zone = 3
				else:
					zone = 4



				if zone == R.zone: # if the closest home marker is less than 2.5m away
					state = "dropping" # set state to dropping
					speed(0, [0, 1])

			else:
				state = "finding home"

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

		speed(-1, [0, 1], True, 0.2)
		speed(1, [0], True, 0.3)
		state = old_state

	if (state == "avoiding collision right"):
		print(state)

		speed(-1, [0, 1], True, 0.2)
		speed(1, [1], True, 0.3)
		state = old_state

	R.sleep(0.2)
	print(bearing)