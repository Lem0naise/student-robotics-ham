from sr.robot3 import *
from operator import attrgetter
from random import randrange
import numpy as np
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

WALL_1 = [x for x in range(7)];
WALL_2 = [x for x in range(7, 14)];
WALL_3 = [x for x in range(14, 21)];
WALL_4 = [x for x in range(21, 28)];

HOME_MARKERS = ZONE_TO_MARKER[R.zone] # Automatically change R.zone when our zone changes in the competition
CLOCKWISE_MARKERS = ZONE_TO_MARKER[(R.zone + 1) % 4]
ANTICLOCKWISE_MARKERS = ZONE_TO_MARKER[(R.zone - 1) % 4]
DIAGONAL_MARKERS = ZONE_TO_MARKER[(R.zone + 2) % 4]

print(R.zone, HOME_MARKERS)

# set OTHER_MARKERS to all wall markers other than [home markers and centre markers]
OTHER_MARKERS = [x for x in range(26) if (x not in HOME_MARKERS) and (x not in [3, 10, 17, 24])]

# all token markers have id of 99
TOKEN_MARKERS = [99]

ARENA_SIDE_LENGTH = 5750

DIST_BETWEEN_ZONE_MARKERS = 718

bearing = 360 - 90*(R.zone + 1) # Change this by 90 since we can face any way in the competition

if R.zone == 0:
	coords = [ARENA_SIDE_LENGTH / 2 - 500, 500]
elif R.zone == 1:
	coords = [ARENA_SIDE_LENGTH, ARENA_SIDE_LENGTH / 2 - 500]
elif R.zone == 2:
	coords = [ARENA_SIDE_LENGTH / 2 + 500, ARENA_SIDE_LENGTH - 500]
else:
	coords = [500, ARENA_SIDE_LENGTH / 2 + 500]

IDEAL_BEARING = (bearing + 90) % 360 # zone closest to us
OTHER_POSSIBLE_BEARING = (bearing - 90) % 360 # zone second closest to us

SPEED = 0 # Millimetres travelled in 1 second at max speed

SLOWER_POWER = 0.7
# ---------- DEGREE AND RADIAN FUNCTIONS ----------
# These already exist under math library but why not make our own
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


#-----------ZONE FUNCTION-----------
#returns which zone you are currently in
def zone(coords):
	if coords[0] < ARENA_SIDE_LENGTH / 2 and coords[1] < ARENA_SIDE_LENGTH / 2:
		return 0
	elif coords[0] > ARENA_SIDE_LENGTH / 2 and coords[1] < ARENA_SIDE_LENGTH / 2:
		return 1
	elif coords[0] > ARENA_SIDE_LENGTH / 2 and coords[1] > ARENA_SIDE_LENGTH / 2:
		return 2
	else:
		return 3
	

# -------- CUBE LOCATION FUNCTION ------
def cubecoords(cube, coords, bearing):
	cube_bearing = (bearing + math.degrees(cube.spherical.rot_y)) % 360
	return [coords[0] + cube.distance * math.cos(math.radians(bearing)), coords[1] + cube.distance * -1 * math.sin(math.radians(bearing))]

# ---------- TURN FUNCTION ---------

TURN_VALUE = 0.005 # the value to change degrees into seconds

# Great function here
def ChangeCoordSystem(gewowioijgr):
	return [gewowioijgr[0], ARENA_SIDE_LENGTH - gewowioijgr[1]]



# This needs changing: to do list
# Change the turn value based on average difference between triangulate bearing and predicted bearing
# Factor in time for motors to get up to speed
def turn(angle):
	global bearing
	if angle > 0: # turning right
		speed(0.5, [0]) 
		speed(0, [1]) 
	else: # turning left
		speed(0, [0]) 
		speed(0.5, [1])

	R.sleep(TURN_VALUE * abs(angle)) # wait until turned angle
	bearing = (bearing - angle) % 360
	speed(0, [0, 1]) # stop both



# Mess of navigation functions here, TriangulateComplicate is the only reliable one at the moment
def Biangulate(each):
	# global bearing
	# northcorrection = bearing
	# wallno = each.id // 7
	# distance = each.distance
	# angle = math.radians(math.degrees(each.spherical.rot_y) + bearing)
	# x_total = 0
	# y_total = 0
	# if each.spherical.rot_y < 0:
	# 	angle = math.radians(math.degrees(-1 * each.spherical.rot_y) + bearing)

	# if wallno == 0:
	# 	#print(each.id)
	# 		#print('POSITIVE ANGLE')
	# 		#print(distance, angle, math.sin(angle))
	# 	x_distance = - 1 * distance * math.sin(angle) + DIST_BETWEEN_ZONE_MARKERS * (each.id + 1)
	# 	y_distance = distance * math.cos(abs(angle))

	# elif wallno == 1:

	# 	y_distance = -1 * distance * math.sin(angle) + DIST_BETWEEN_ZONE_MARKERS * (each.id - 6)
	# 	x_distance = ARENA_SIDE_LENGTH - distance * math.cos(abs(angle))
	
	# elif wallno == 2:
	# 	x_distance = ARENA_SIDE_LENGTH - distance * math.sin(angle) - DIST_BETWEEN_ZONE_MARKERS * (each.id - 13)
	# 	y_distance = ARENA_SIDE_LENGTH - distance * math.cos(abs(angle))

	# elif wallno == 3:
	# 	y_distance = ARENA_SIDE_LENGTH - distance * math.sin(angle) - DIST_BETWEEN_ZONE_MARKERS * (each.id - 20)
	# 	x_distance = distance * math.cos(abs(angle))
	
	# if x_distance < 0:
	# 	x_distance *= -1
	# if y_distance < 0:
	# 	y_distance *= -1


	# global bearing
	# markerlist = [[(i+1)*DIST_BETWEEN_ZONE_MARKERS,0] for i in range(7)]
	# for i in range(7):
	# 	markvec = [ARENA_SIDE_LENGTH,(i+1)*DIST_BETWEEN_ZONE_MARKERS]
	# 	markerlist.append(markvec)
	# for i in range(7):
	# 	markvec = [ARENA_SIDE_LENGTH-((i+1)*DIST_BETWEEN_ZONE_MARKERS),ARENA_SIDE_LENGTH]
	# 	markerlist.append(markvec)
	# for i in range(7):
	# 	markvec = [0,ARENA_SIDE_LENGTH-((i+1)*DIST_BETWEEN_ZONE_MARKERS)]
	# 	markerlist.append(markvec)	
	# markx = markerlist[each.id][0]
	# marky = markerlist[each.id][1]	
	# distancetomarker = each.distance
	# angletomarker = (360 - math.degrees(each.spherical.rot_y)) % 360
	# theta = math.radians((bearing + angletomarker)%360)
	# print('bearing = ', bearing)
	# print('theta = ', math.degrees(theta))
	# print('distance = ', distancetomarker)
	# x = distancetomarker * math.cos(theta)
	# y = distancetomarker * math.sin(theta)
	# xcoord = markx - x
	# ycoord = marky + y

	# return xcoord, ycoord
	pass

cubes_taken = 0
def Triangulate():
	global bearing
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
			marker1 = new_cubes[0]
			marker2 = new_cubes[1]

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
		markdist = ((vector1[0]-vector2[0])**2+(vector1[1]-vector2[1])**2)**0.5
		s = (dist1+dist2+markdist)/2
		area = (s*(s-dist1)*(s-dist2)*(s-markdist))**0.5
		
		perpdist = area/(0.5*markdist)
		marker1radius = dist1
		marker2radius = dist2
		linegradient = (vector2[1] - vector1[1]) / (vector2[0] - vector1[0])
		
		# wallno = id1//7

		# if wallno%2==0:
		# 	if wallno==0:
		# 		y = perpdist
		# 	else:
		# 		y = ARENA_SIDE_LENGTH - perpdist
		# 	x1 = vector1[0]
		# 	x2 = vector2[0]
		# 	xdist1a = (dist1**2 - perpdist**2)**0.5
		# 	xdist1b = -xdist1a
		# 	xdist2a = (dist2**2 - perpdist**2)**0.5
		# 	xdist2b = -xdist2a
		# 	poss0 = abs((x1+xdist1a)-(x2+xdist2a))
		# 	poss1 = abs((x1+xdist1b)-(x2+xdist2a))
		# 	poss2 = abs((x1+xdist1a)-(x2+xdist2b))
		# 	poss3 = abs((x1+xdist1b)-(x2+xdist2b))
		# 	posslist = [poss0,poss1,poss2,poss3]
		# 	minposs = posslist.index(min(posslist))
		# 	if poss0 < poss1 and poss0 < poss2 and poss0 < poss3:
		# 		x = ((x1+xdist1a)+(x2+xdist2a))/2
		# 	elif poss1 < poss0 and poss1 < poss2 and poss1 < poss3:
		# 		x = ((x1+xdist1b)+(x2+xdist2a))/2
		# 	elif poss2 < poss0 and poss2 < poss1 and poss2 < poss3:
		# 		x = ((x1+xdist1a)+(x2+xdist2b))/2
		# 	elif poss3 < poss0 and poss3 < poss2 and poss3 < poss1:
		# 		x = ((x1+xdist1b)+(x2+xdist2b))/2
		# 	return [x,y]

		# else:
		# 	if wallno==1:
		# 		x = ARENA_SIDE_LENGTH - perpdist
		# 	else:
		# 		x = perpdist
		# 	y1 = vector1[1]
		# 	y2 = vector2[1]
		# 	ydist1a = (dist1**2 - perpdist**2)**0.5
		# 	ydist1b = -ydist1a
		# 	ydist2a = (dist2**2 - perpdist**2)**0.5
		# 	ydist2b = -ydist2a
		# 	poss0 = abs((y1+ydist1a)-(y2+ydist2a))
		# 	poss1 = abs((y1+ydist1b)-(y2+ydist2a))
		# 	poss2 = abs((y1+ydist1a)-(y2+ydist2b))
		# 	poss3 = abs((y1+ydist1b)-(y2+ydist2b))
		# 	posslist = [poss0,poss1,poss2,poss3]
		# 	minposs = posslist.index(min(posslist))
		# 	if minposs==0:
		# 		y = ((y1+ydist1a)+(y2+ydist2a))/2
		# 	elif minposs==1:
		# 		y = ((y1+ydist1b)+(y2+ydist2a))/2
		# 	elif minposs==2:
		# 		y = ((y1+ydist1a)+(y2+ydist2b))/2
		# 	elif minposs==3:
		# 		y = ((y1+ydist1b)+(y2+ydist2b))/2
		# 	return [x,y]
def Magnitude(vector):
	return (vector[0] ** 2 + vector[1] ** 2)**(1/2)

def Arctan(x):
	if math.atan(x) < 0:
		return math.atan(x)+(math.pi)
	else:
		return math.atan(x)	       

def RotateVector(vec, angle):
	newVec = [vec[0] * math.cos(angle) + vec[1] * -1 * math.sin(angle), vec[0] * math.sin(angle) + vec[1] * math.cos(angle)]
	return newVec


def TriangulateComplicate(cubes=None): 
	if cubes == None:
		cubes = R.camera.see()
	new_cubes = []
	for each in cubes:
		if each.id in range(0, 27):
			new_cubes.append(each)
	if len(new_cubes) > 1:
		marker1 = new_cubes[0]
		marker2 = new_cubes[1]
		marker1angle = marker1.spherical.rot_y
		marker2angle = marker2.spherical.rot_y
		if marker1angle > marker2angle:
			marker2 = new_cubes[0]
			marker1 = new_cubes[1]
			marker1angle = marker1.spherical.rot_y
			marker2angle = marker2.spherical.rot_y
		markerlist = [ChangeCoordSystem([(i+1)*DIST_BETWEEN_ZONE_MARKERS,0]) for i in range(7)]
		for i in range(7):
			markvec = [ARENA_SIDE_LENGTH,(i+1)*DIST_BETWEEN_ZONE_MARKERS]
			markerlist.append(ChangeCoordSystem(markvec))
		for i in range(7):
			markvec = [ARENA_SIDE_LENGTH-((i+1)*DIST_BETWEEN_ZONE_MARKERS),ARENA_SIDE_LENGTH]
			markerlist.append(ChangeCoordSystem(markvec))
		for i in range(7):
			markvec = [0,ARENA_SIDE_LENGTH-((i+1)*DIST_BETWEEN_ZONE_MARKERS)]
			markerlist.append(ChangeCoordSystem(markvec))
		marker1vec = markerlist[marker1.id]
		marker2vec = markerlist[marker2.id]
		veca = [(marker2vec[0] - marker1vec[0]),(marker2vec[1] - marker1vec[1])]
		ax = veca[0]
		ay = veca[1]
		a = Magnitude(veca)
		b = marker1.distance
		c = marker2.distance
		costheta = (a**2 + b**2 - c**2)/(2*a*b)
		theta = math.acos(costheta)
		veca[0] *= b / a
		veca[1] *= b / a
		theta = 2*math.pi - theta
		vecb = RotateVector(veca, theta)
		bcoord = [marker1vec[0] + vecb[0], marker1vec[1] + vecb[1]]

		bx = (marker1vec[0] - bcoord[0])
		by = (marker1vec[1] - bcoord[1])
		costheta = bx / b
		sintheta = by / b
		a = math.acos(costheta)
		b = 2 * math.pi - a
		c = math.asin(sintheta)
		d = math.pi - c
		if c < 0:
			c += 2*math.pi
		if d < 0:
			d += 2*math.pi
		acdiff = abs(a - c)
		addiff = abs(a - d)
		bcdiff = abs(b - c)
		bddiff = abs(b - d)
		difflist = [acdiff, addiff, bcdiff, bddiff]
		difflist.sort()
		if difflist[0] == acdiff:
			bearing = (a + c) / 2
		elif difflist[0] == addiff:
			bearing = (a + d) / 2
		elif difflist[0] == bcdiff:
			bearing = (b + c) / 2
		else:
			bearing = (b + d) / 2
		bearing += marker1angle
		bearing = bearing%(2*math.pi)
		bearing = math.degrees(bearing)
		bcoord = ChangeCoordSystem(bcoord)
		return bcoord, bearing


# ---------- MAIN PROGRAM ---------
# This was for virtual competition - we cannot grab gold any more
# R.servo_board.servos[0].position = -1
# R.servo_board.servos[1].position = -1
# turn(-90) # very initial turn
# speed(1, [0, 1])
# R.sleep(0.5)
# turn(35)
# speed(1, [0, 1])
# R.sleep(0.3)
# turn(115)	
# speed(1, [0, 1])
# R.sleep(0.8)
# turn(35)
# stopped = False
# while not stopped:
# 	speed(1, [0, 1]) # full speed
# 	R.sleep(0.1)

# 	m_angle = marker_angle(TOKEN_MARKERS) # check angle to the closest marker
	
# 	if m_angle == None: # if for some reason have completely lost sight of marker
# 		pass
		
# 	else:
# 		if m_angle >= 5 or m_angle <= -5: # if the angle of deviation is enough to care about
# 			turn(m_angle)
# 	if dist_front() < 0.11 or dist_front() > 1.99: # if about to hit it     
# 		speed(0.2, [0, 1]) # stop
# 		stopped = True
# R.sleep(0.1)
# R.servo_board.servos[0].position = 1
# R.servo_board.servos[1].position = 1
# R.sleep(0.2)
# speed(-1, [0, 1])
# R.sleep(0.5)
# R.servo_board.servos[0].position = -1
# R.servo_board.servos[1].position = -1
# R.sleep(0.3)
# turn(15)
# speed(1, [0, 1])
# R.sleep(0.6)
# speed(0.2, [0, 1])
# R.sleep(0.1)
# if dist_front() < 0.12:
# 	R.servo_board.servos[0].position = 1
# 	R.servo_board.servos[1].position = 1
# else:
# 	speed(1, [0, 1])
# 	R.sleep(0.7)
# 	R.servo_board.servos[0].position = 1
# 	R.servo_board.servos[1].position = 1
# R.sleep(0.2)
# speed(-1, [0, 1])
# R.sleep(2.4)
# speed(1, [0, 1])
# turn(300)
# speed(1, [0, 1])
# R.sleep(3.4)
# R.servo_board.servos[0].position = -1
# R.servo_board.servos[1].position = -1
# speed(-1, [0, 1])
# R.sleep(0.3)
# R.servo_board.servos[0].position = 1
# R.servo_board.servos[1].position = 1
# R.sleep(0.2)
# R.servo_board.servos[0].position = -1
# R.servo_board.servos[1].position = -1
# R.sleep(0.5)
# turn(-270)
# speed(1, [0, 1])
# R.sleep(0.47)
state = 'stationary'
count = 0
grabbed = 0
last_zone = (R.zone - 1) % 4
zone_targetting = (R.zone + 1) % 4
same_state_count = 0
#Idea: alternate between which zones we target
while True:
	
	print(state) # logging state to console
	# -------- SETUP --------
	# -------- SETTING VIEW TO FIND MARKERS NOT IN HOME ZONE ---------
	if (state == "stationary"):		
		if zone_targetting == (R.zone + 1) % 4:
			target_bearing = IDEAL_BEARING
		else:
			target_bearing = OTHER_POSSIBLE_BEARING
		new_bearing = (bearing - target_bearing) % 360
		if new_bearing > 180:
			turn(new_bearing - 360)
		else:
			turn(new_bearing)
		state = "moving to enemy zone"


	# -------- FINDING TOKEN MARKERS --------

	elif (state == "looking"):

		R.sleep(0.05) # pause before looking
		
		cubes = R.camera.see() # make list of all visible cubes
		pos = TriangulateComplicate(cubes)
		if pos != None:
			if zone(pos) == R.zone: # add more conditions like num of cubes grabbed
				state = 'moving'
		if len(cubes) > 0 and state == 'looking': # if can see any cubes
			closest = None
			markers = R.camera.see() 
			for m in markers:
				if m.id > 27 and m.cubecoords
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
			

			if dist_front() < 0.15: # if about to hit it     
				speed(0, [0, 1]) # stop


				closest_marker = marker(TOKEN_MARKERS)
				if closest_marker:
					if closest_marker.distance <= 400: # if about to grab a token and not a wall or other bot
						state = "grabbing"
					else:
						state = "empty"


	#----MOVING TO ENEMY ZONE---
	elif state == 'moving to enemy zone':
		same_state_count += 1
		pos = TriangulateComplicate()
		if pos != None:
			bearing = pos[1]
			zone = zone(pos[0])
			if same_state_count == 10:
				state = 'looking'
			if zone == (R.zone + 1) % 4 or zone == (R.zone - 1) % 4:
				state = 'looking'
			elif zone == (R.zone + 2) % 4:
				state = 'escape'
		elif state == 'moving to enemy zone':
			m_angle = marker_angle(TOKEN_MARKERS) # check angle to the closest marker
		
			if m_angle == None: # no cubes to bump into
				speed(1, [0, 1])
# Note: If motor[1] is slower, it turns clockwise, else anticlockwise			
			else:
				if m_angle >= 10 or m_angle <= -10: # if we are going to hit the cube (in our zone)
					if m_angle >= 0:
						speed(SLOWER_POWER, [1])
						R.sleep(0.2)
						speed(1, [0, 1])
					else:
						speed(SLOWER_POWER, [0])
						R.sleep(0.2)
						speed(1, [0, 1])

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

			turn(-15)
			total_turned += 15

		
		if h_angle != None: # if we found a home marker
			h_marker = marker(HOME_MARKERS)
			if h_marker != None:
				id = h_marker.id
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
				markvec = markerlist[id]
				if markvec[1]==0 or markvec[1]==ARENA_SIDE_LENGTH:
					criticaldistance = abs(2875 -markvec[0])+300
				else:
					criticaldistance = abs(2875 -markvec[1])+300
				if h_marker.distance < criticaldistance:
					state = "dropping" # set state to dropping
					speed(0, [0, 1])
				else:
					turn(h_angle)
					state = "returning"
			else:
				turn(h_angle) # turn the angle of the closest home marker

				state = "returning"

		elif total_turned >= 360: # if instead we turned a full circle
			speed(-1, [0, 1], True, 0.3)
			speed(0, [0, 1])


	# -------- RETURNING BACK TO HOME WITH A TOKEN ---------
	elif (state == "returning"):

		speed(1, [0, 1])
		R.sleep(2)
		speed(0, [0, 1])
		state = 'dropping'
		# h_marker = marker(HOME_MARKERS)
		# if h_marker != None: # if seen a home marker
		# 	id = h_marker.id
		# 	markerlist = [[(i+1)*DIST_BETWEEN_ZONE_MARKERS,0] for i in range(7)]
		# 	for i in range(7):
		# 		markvec = [ARENA_SIDE_LENGTH,(i+1)*DIST_BETWEEN_ZONE_MARKERS]
		# 		markerlist.append(markvec)
		# 	for i in range(7):
		# 		markvec = [ARENA_SIDE_LENGTH-((i+1)*DIST_BETWEEN_ZONE_MARKERS),ARENA_SIDE_LENGTH]
		# 		markerlist.append(markvec)
		# 	for i in range(7):
		# 		markvec = [0,ARENA_SIDE_LENGTH-((i+1)*DIST_BETWEEN_ZONE_MARKERS)]
		# 		markerlist.append(markvec)
		# 	markvec = markerlist[id]
		# 	if markvec[1]==0 or markvec[1]==ARENA_SIDE_LENGTH:
		# 		criticaldistance = abs(2875 -markvec[0])-100
		# 	else:
		# 		criticaldistance = abs(2875 -markvec[1])-100
		# 	if h_marker.distance < criticaldistance:
		# 		state = "dropping" # set state to dropping
		# 		speed(0, [0, 1])

		# else: # if cannot see a home marker

		# 	state = "finding home"



	# -------- DROPPING OFF TOKEN ---------

	elif (state == "dropping"):
		cubes_taken += 1
		# release 
		R.servo_board.servos[0].position = -1
		R.servo_board.servos[1].position = -1

		R.sleep(0.2)
		speed(-1, [0, 1], True, 0.2) # reverse
		turn(180)
		state = "stationary" # reset to looking for markers


	# -------- REVERSING -------------------
	elif (state == "reversing"):
		speed(-1, [0, 1], True, 0.7)
		speed(0, [0, 1])
		state = "stationary"
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

