To run the code
```
$ roscore
$ roslaunch turtlebot_bringup minimal.launch
$ roslaunch astra_launch astra_pro.launch
```

Then,
```
$ roscd cmvision
$ rosparam set /cmvision/color_file /home/turtlebot/colors.txt
$ rosrun cmvision cmvision image:=/camera/rgb/image_raw
```

```
$ cd ~/catkin_ws/src/where_is_blob/src
$ python color_tracker.py
```
