# $ roscore
# $ roslaunch turtlebot_bringup minimal.launch
# $ roslaunch astra_launch astra_pro.launch

# Calibrate color in ~/colors.txt
# $ roscd cmvision
# $ roslaunch cmvision cmvision.launch image:=/camera/rgb/image_raw
# << CTRL+C to kill process >>
# $ rosparam set /cmvision/color_file ~/colors.txt
# $ rosrun cmvision cmvision image:=/camera/rgb/image_raw

# $ cd ~/catkin_ws/src/where_is_blob/src
# $ python color_tracker.py

# Blob callback is working!! Now we have to:
# TODO: How to calibrate properly? Our gui shows AB instead of YUV

import roslib
import rospy
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob
from create_node.msg import TurtlebotSensorState

# global
turn = 0.0 #turning rate
blob_position = 0 # x position for the blob

def callback(data):
  global turn
  global blob_position

  if len(data.blobs):
    rospy.loginfo('FOUND BLOB!!!')
    turn = 0.5
  else:
    rospy.loginfo('Looking for blob... %s' % data.blobs)
    turn = 0.1

def run():
  global blob_position

  # publish twist messages to /cmd_vel
  pub = rospy.Publisher('/mobile_base/commands/velocity', Twist)

  #subscribe to the robot sensor state
  rospy.Subscriber('/blobs', Blobs, callback)
  rospy.init_node("color_tracker")

  global turn
  twist = Twist()

  while not rospy.is_shutdown():

    # use turn to turn the robot slower/faster
    twist.linear.x = 0.0; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = turn

    # publish turn
    pub.publish(twist)
    rospy.sleep(0.1)

if __name__ == '__main__':
  try:
    run()
  except rospy.ROSInterruptException:
    print('OMG')
