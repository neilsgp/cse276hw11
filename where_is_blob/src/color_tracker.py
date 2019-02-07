# CSE 276B - HW 6
# Authors: Neil Sengupta, Hadi Givehchian, Gustavo Umbelino
# References:
# # Python color-tracking: http://www.transistor.io/color-blob-tracking-with-ros.html

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

import roslib
import rospy
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

  if backing_up:
    return

  # if a blob is found...
  if len(data.blobs):

    # take average of blob positions
    for blob in data.blobs:
      blob_position += blob.x
    blob_position /= len(data.blobs)

    # log message
    rospy.loginfo('FOUND %d BLOB(S) at position %.2f' % (len(data.blobs), blob_position))

    # turn anti-clockwise
    if blob_position > 450:
      turn = -0.5
      rospy.loginfo('Move to left!')
      forward = 0

    # turn clockwise
    if blob_position < 200:
      turn = 0.1
      forward = 0

    # perfect, move forward!
    if blob_position > 200 and blob_position < 450:
      turn = 0
      forward = 0.1

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
  if n > 4000:
    x /= n
    y /= n
    z /= n

    rospy.loginfo('Centroid (n = %d) at (%.2f, %.2f, %.2f)' % (n, x, y, z))

    # too close!! avoid obstacle fast!!
    if z < 0.6 or backing_up:
      backing_up = True
      handle_obstacle()    
  
  # not enough points detected
  else:
    rospy.loginfo('Not enough points detected: %d' % n)

# subscribe
def run():
  global blob_position
  global turn
  global forward

  # publish twist messages to /cmd_vel
  pub = rospy.Publisher('/mobile_base/commands/velocity', Twist)

  # subscribe to topics
  rospy.Subscriber('/blobs', Blobs, callback)
  rospy.Subscriber('/camera/depth/points', PointCloud2, pcl_callback)

  rospy.init_node("color_tracker")
  rospy.wait_for_message('/camera/depth/points', PointCloud2)

  # create twist instance
  twist = Twist()

  # run this while kobuki is on...
  while not rospy.is_shutdown():

    # use turn to turn the robot slower/faster
    twist.linear.x = forward; twist.linear.y = forward; twist.linear.z = forward
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = turn

    # publish turn
    pub.publish(twist)
    blob_position = 0
    rospy.sleep(0.1)

# main function
if __name__ == '__main__':
  try:
    run()
  except rospy.ROSInterruptException:
    print('OMG')
