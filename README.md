## Authors
Gustavo, Hadi, Neil 

## Compile and run code
First run dependent services
```
$ roscore
$ roslaunch turtlebot_bringup minimal.launch
$ roslaunch astra_launch astra_pro.launch
```

Run `cmvision`,
```
$ roscd cmvision
$ rosparam set /cmvision/color_file /home/turtlebot/colors.txt
$ rosrun cmvision cmvision image:=/camera/rgb/image_raw
```

Run the project using
```
$ cd ~/catkin_ws/src/where_is_blob/src
$ python color_tracker.py
```

## FSM Diagram
<img src="https://puu.sh/CIKO5/46145c82d4.png" alt="Kitten"
	title="FSM Diagram" width="300" height="400" />

Our robot is stationary at first. When, we start `color_tracker.py`
the robot twists continuously until it can find the blob. Our blob is callibrated
using the green board in `colors.txt`. Once the blob is found, Kuboki
moves towards the blob with a preset velocity. If at any point the blob
isn't found, it twists to look for the blob. If there is an obstacle 
it moves to evade it and look for the blob continuously. Once it reaches
the goal it stops.
