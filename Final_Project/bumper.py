#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
import time 

bumps = False

def callback(data):
    global bumps
    if data.bumper == 1:
        bumps = not bumps
        print "bump"

def talker():
	print "in talker"

	pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
	bumper = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callback)
	rospy.init_node('talker', anonymous=True)
	r = rospy.Rate(1) 
	t_end = time.time() + 60 * 1

	while time.time() < t_end:
		global bumps
		if bumps:
			print "bumper"
			bumps = not bumps
        r.sleep()
	
	print "exiting game"

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass