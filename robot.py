import time

from sr.robot import *

R = Robot()

time.sleep(3)

print("I see {} things".format(len(R.see())))


# motor board 0, channel 0 to half power forward
R.motors[0].m0.power = 50

# motor board 0, channel 1 to half power forward
R.motors[0].m1.power = 50

# sleep for 1 second
time.sleep(1)

# motor board 0, channel 0 to stopped
R.motors[0].m0.power = 0

# motor board 0, channel 1 to stopped
R.motors[0].m1.power = 0

# sleep for 2 seconds
time.sleep(2)

# motor board 0, channel 0 to half power backward
R.motors[0].m0.power = -50

# motor board 0, channel 1 to half power forward
R.motors[0].m1.power = 50

# sleep for 0.75 seconds
time.sleep(0.75)

# motor board 0, channel 0 to half power forward
R.motors[0].m0.power = 50

# motor board 0, channel 1 to half power forward
R.motors[0].m1.power = 50

# sleep for 1 second
time.sleep(1)

# motor board 0, channel 0 to stopped
R.motors[0].m0.power = 0

# motor board 0, channel 1 to stopped
R.motors[0].m1.power = 0



i = 0

#define functions

#function to turn on the spot (to turn opposite input -power)
#Variable affix T
def turnOnSpot(powerT, timeT):
    R.motors[0].m0.power = powerT
    R.motors[0].m1.power = powerT
    R.motors[1].m0.power = powerT
    time.sleep(timeT)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    R.motors[1].m0.power = 0
    
#Function to go forwards or backwards
#Variable affix X
def goStraight(powerX, timeX):
    R.motors[0].m0.power = powerX
    R.motors[0].m1.power = powerX
    time.sleep(timeX)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

#goto func
def go_to():
    turnamount = None
    distance = 0
    #check camera 
    markers = R.see()
    for m in markers:
        turnamount = m.rot_y
        distance = m.dist
        print "turn", turnamount
        print "dist", distance
        
    #rotate 
    BLMotor = 40 #back left
    BRMotor = -42 #back right
    FMotor = 0 #front
    if turnamount == None:
        print "turn none"
    elif turnamount > 3:
        #Turn right
        FMotor = 20
        BRMotor = 20
        BLMotor = 20
        print "going right"
    elif turnamount < -3:
        #Turn left
        FMotor = -20
        BLMotor = -20
        BRMotot = 20
        print "going left" 
    
    R.motors[0].m0.power = BLMotor
    R.motors[0].m1.power = BRMotor
    R.motors[1].m0.power = FMotor
    
    #Limit Distance 
    if distance > 1.5:
            distance = 1.5
            
    #Determine Wait
    if FMotor == 0:
        #Moves forward for the distance away from box in meters seconds but max 1.5 seonds
        time.sleep(distance)
    else:
        #turns 0.02*turn from y / distance from the box
        turnsleep = 0.02*abs(turnamount)
        if distance > 1:
            turnsleep = turnsleep/distance
        elif distance < 1:
            turnsleep = turnsleep*distance
            
        time.sleep(turnsleep)
    
    #stopforphoto
    R.motors[0].m0.power = -BLMotor/2
    R.motors[0].m1.power = -BRMotor/2
    R.motors[1].m0.power = -FMotor/2
    time.sleep(0.01)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    R.motors[1].m0.power = 0
    
def capture_box():
    R.motors[0].m0.power = 40
    R.motors[0].m1.power = 40
    R.motors[1].m0.power = 40
    time.sleep(1.7)
    R.motors[0].m0.power = -40
    R.motors[0].m1.power = 40
    R.motors[1].m0.power = 0
    time.sleep(1)

# MAIN FUNCTION
i = 0
sure = 0

while i < 1000:

    #Check camera 
    markers = R.see()
    markertype = None
    for m in markers:
        markertype = m.info.marker_type
        distance = m.dist 
        
    print markertype
    print markers
        
    if markertype == MarkerType.SILVER:
        go_to()
        if distance < 0.5:
            capture_box()
    
    time.sleep(0.5)
    i = i + 1 

