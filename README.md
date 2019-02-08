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

## Testing 
We conducted several experiments to test the performance of our robot. We will briefly explain the most important experiments below. For the first part, we just tested the robot while there is no obstacle in the way and someone is holding the goal `move_to_goal_demo` and the goal is attached to the cabinet `move_to_goal_demo2`. 
For the second part in which the robot should avoid the obstacle and then try to find the goal again and move towards the goal, we did 2 experiments. In `obstacle_human_demo` video, a human’s feet is considered as an obstacle. In this case, the robot can see some parts of the goal from between human legs. In `obstacle_box_demo` video, the robot can’t see any part of the goal at first, so it tries to move and search for the goal.

## Videos
The videos are [here](https://drive.google.com/drive/u/0/folders/1-3IwQXM2ItUJVxufwHA_2_u3-H-KgRv0)
