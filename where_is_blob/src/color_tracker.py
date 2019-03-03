# CSE 276B - HW 11
# Authors: Neil Sengupta, Hadi Givehchian, Gustavo Umbelino
# References:
# # Python color-tracking: http://www.transistor.io/color-blob-tracking-with-ros.html
# # ROS Perception: https://github.com/gertanoh/ROS-Perception

# $ roscore
# $ roslaunch turtlebot_bringup minimal.launch
# $ roslaunch astra_launch astra_pro.launch

# Calibrate color in ~/colors.txt
# $ roscd cmvision
# $ roslaunch cmvision cmvision.launch image:=/camera/rgb/image_raw
# << CTRL+C to kill process >>
# $ rosparam set /cmvision/color_file /home/turtlebot/colors.txt
# $ rosrun cmvision cmvision image:=/camera/rgb/image_raw

# $ cd ~/catkin_ws/src/where_is_blob/src
# $ python color_tracker.py

#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from math import radians
import os
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob
from create_node.msg import TurtlebotSensorState

# global
turn = 0.0 # turning rate
blob_position = 0 # x position for the blob
forward = 0.0 # speed forward 
backing_up = False
going_straight = False
found_goal = False

# pcl vars
min_x = -0.2
max_x = 0.2
min_y = -0.3
max_y = 0.5
max_z = 1.2

# called within a timer
def timer_callback(event):
  global backing_up 
  backing_up = False
  rospy.loginfo('STOP BACKING UP!!')

# called to handle obstacles
def handle_obstacle():
  global turn
  global forward

  # set back-up turn and speed values
  turn = -1
  forward = -0.1
  
  # let kobuki 
  rospy.Timer(rospy.Duration(0.5), timer_callback, oneshot=True)  

# cmvision callback
# called when a blob is detected
# uses ~/colors.txt 
def callback(data):
  global turn
  global forward
  global blob_position
  global backing_up 
  global found_goal

  if backing_up or found_goal == True:
    return

  # if a blob is found...
  if len(data.blobs):

    # take average of blob positions
    for blob in data.blobs:
      blob_position += blob.x
    blob_position /= len(data.blobs)

    if found_goal == False:
        # log message
        rospy.loginfo('FOUND %d BLOB(S) at position %.2f' % (len(data.blobs), blob_position))

        # message to communicate to human
        os.system("say 'Whats up dude!'")
        os.system("say 'Take my candy!'")

    found_goal = True

  # no blob found...
  else:
    rospy.loginfo('Looking for blob... spinning')
    forward = 0.0
    turn = 0.3


# called when point is detected
def pcl_callback(data):
  global min_x
  global max_x
  global min_y
  global max_y
  global max_z
  global backing_up 
  global going_straight

  # init values
  x = y = z = n  = 0

  # go through all points detected
  for point in point_cloud2.read_points(data, skip_nans=True):
    pt_x = point[0]
    pt_y = point[1]
    pt_z = point[2]

    # filter points according to window size
    if -pt_y > min_y and -pt_y < max_y and pt_x < max_x and pt_x > min_x and pt_z < max_z:
      x += pt_x
      y += pt_y
      z += pt_z
      n += 1
    
  # calculate centroid
  if (going_straight == False and n > 4000):
    x /= n
    y /= n
    z /= n

    rospy.loginfo('Centroid (n = %d) at (%.2f, %.2f, %.2f)' % (n, x, y, z))

    # too close!! avoid obstacle fast!!
    if z < 0.8 or backing_up:
      backing_up = True
      print ("door detected")
      handle_obstacle()    
  
  # not enough points detected
  else:
    rospy.loginfo('Not enough points detected: %d' % n)


class DrawASquare():
    def __init__(self):
        global blob_position
        global turn
        global forward
        global going_straight
        global found_goal

        # initiliaze
        rospy.init_node('drawasquare', anonymous=False)

        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

        rospy.Subscriber('/blobs', Blobs, callback)
        rospy.Subscriber('/camera/depth/points', PointCloud2, pcl_callback)

        # rospy.init_node("color_tracker")
        rospy.wait_for_message('/camera/depth/points', PointCloud2)
     
	# 5 HZ
        r = rospy.Rate(5);

	# create two different Twist() variables.  One for moving forward.  One for turning 45 degrees.
        move_cmd = Twist()
        move_cmd.linear.x = 0.2

        #let's turn at 45 deg/s
        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = radians(60); #45 deg/s in radians/s
        
        #let's turn at 45 deg/s
        neg_turn_cmd = Twist()
        neg_turn_cmd.linear.x = 0
        neg_turn_cmd.angular.z = radians(64); #45 deg/s in radians/s
        
        #let's turn at 45 deg/s
        twice_turn_cmd = Twist()
        twice_turn_cmd.linear.x = 0
        twice_turn_cmd.angular.z = radians(-120); #45 deg/s in radians/s

        count = 0

        while not rospy.is_shutdown():

            # found goal, don't move
            if found_goal == True:
                for x in range(0,20):
                    self.cmd_vel.publish(Twist())
                    r.sleep()
                found_goal = False

        
	    # go forward 0.4 m (2 seconds * 0.2 m / seconds)
            rospy.loginfo("Going Straight")
            going_straight = True
            for x in range(0,20):
                self.cmd_vel.publish(move_cmd)
                r.sleep()
	        
            if(count % 3 == 0):
                os.system("say 'Where are you human?'")

        # turn 90 degrees
	        rospy.loginfo("Turning left")
            going_straight = False
            for x in range(0,10):
                self.cmd_vel.publish(turn_cmd)
                r.sleep()            	    

        # turn 180 degrees
	        rospy.loginfo("Turning right")
            going_straight = False
            for x in range(0,10):
                self.cmd_vel.publish(twice_turn_cmd)
                r.sleep()            
       
        # turn -90 degrees
	        rospy.loginfo("Turning forward")
            going_straight = False
            for x in range(0,10):
                self.cmd_vel.publish(neg_turn_cmd)
                r.sleep()     
    
            count = count+1
            

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop Drawing Squares")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    DrawASquare()



