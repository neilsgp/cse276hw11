#! /usr/bin/env python

# CSE 276B - Final Presentation
# Authors: Neil Sengupta, Hadi Givehchian, Gustavo Umbelino
# References:
# # Python color-tracking: http://www.transistor.io/color-blob-tracking-with-ros.html
# # ROS Perception: https://github.com/gertanoh/ROS-Perception

import rospy
import actionlib
import time
import os
import speech_recognition as sr
import webbrowser
import random
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
from cmvision.msg import Blobs, Blob
from kobuki_msgs.msg import BumperEvent


# H O W   T O   R U N   A L F R E D
# $ roscore
# $ roslaunch turtlebot_bringup minimal.launch

# $ roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/turtlebot/Desktop/alfreddemo.yaml
# $ roslaunch turtlebot_rviz_launchers view_navigation.launch

# $ roslaunch cmvision cmvision.launch image:=/camera/rgb/image_raw
# << CTRL+C to kill process >>
# $ rosparam set /cmvision/color_file /home/turtlebot/colors.txt
# $ rosrun cmvision cmvision image:=/camera/rgb/image_raw

# $ cd ~/catkin_ws/src/gaitech_edu/src/turtlebot/navigation/map_navigation/scripts
# $ python map_navigation_gus.py

# Calibrate color in ~/colors.txt

class map_navigation_gus():

	def choose(self):

		choice='q'

		rospy.loginfo("|'0': Lab ")
		rospy.loginfo("|'1': Dean ")
		rospy.loginfo("|'2': Arun Kumar Office ")
		rospy.loginfo("|'3': Nadir Weibel ")
                rospy.loginfo("|'4': Sofa ")
                rospy.loginfo("|'5': Kitchen ")
                rospy.loginfo("|'q': Quit ")
		rospy.loginfo("|WHERE TO GO?")
		choice = input()
		return choice

	def displayPage(self, schoice):
		if (schoice == -1):
			link = 'https://neilsgp.github.io/alfred/index.html'
		elif (schoice == 0):
			link = 'https://neilsgp.github.io/alfred/index.html'
		elif (schoice == 1):
			link = 'https://scholar.google.com/citations?user=BEEuinQAAAAJ&hl=en'
		elif (schoice == 2):
			link = 'http://cseweb.ucsd.edu/~arunkk/'
		elif (schoice == 3):
			link = 'https://ubicomp.ucsd.edu/people/weibel/'
		elif (schoice == 4):
			link = 'https://neilsgp.github.io/alfred/rest.html'
		elif (schoice == 5):
			link = 'https://www.youtube.com/watch?v=05L0hOw2yVs&t=2s'
		elif (schoice == 6):
			link = 'https://www.youtube.com/watch?v=05L0hOw2yVs&t=2s'
		else:
			link = 'https://neilsgp.github.io/alfred/index.html'

		webbrowser.open(link, new=2)

	def Speaking(self, schoice):
		if (schoice == -1):
			var = 'Hello! My name is Kobuki and I will take you in a fabulous adventure. Follow me.'
		elif (schoice == 0):
			var = 'Welcome to the Embedded Systems lab. Please go inside.'
		elif (schoice == 1):
			var = 'Here is Dean Tullsens office. Please knock on the door.'
		elif (schoice == 2):
			var = 'Here is Arun Kumar office'
		elif (schoice == 3):
			var = 'Here is Nadir Weibel office'
		elif (schoice == 4):
			var = 'This is the sofa room. Take a seat, if you want.'
		elif (schoice == 5):
			var = 'Finally, welcome to the kitchen. Are you hungry?'
		elif (schoice == 6):
			var = 'Ok, time to go. Follow me!'

		os.system("say " +  var)
		if schoice == -1:
			self.stopped = True
			time.sleep(5)
			self.stopped = False
		else:
			self.stopped = True
			time.sleep(10)
			self.stopped = False

	def humanGotBored(self):
		self.bored = True
		print('HUMAN GOT BORED!!!!')
		os.system("say 'You seem bored, back up 10 feet and lets play a game!'")

	# called on bumber hit
	def bumper_callback(self, data):
		if not self.bored:
			return

		if data.bumper == 1:
			rand = random.randint(0, 2)
			if rand == 0:
				os.system("say 'Oh my!'")
			elif rand == 1:
				os.system("say 'Stop!'")
			elif rand == 2:
				os.system("say 'That hurts!'")
			else:
				os.system("say 'I dont know what to say!'")

	def blobs_callback(self, data):

		# if a blob is found...
		if self.stopped and len(data.blobs) > 10:
			for blob in data.blobs:
				if blob.name == 'Pink' and blob.area > 38000:
					print('Found %s (%d)' % (blob.name, blob.area))
					if not self.bored:
						self.humanGotBored()

	def playGame(self):
		os.system("say 'Ok, go, kick me!'")
		time.sleep(10)
		# self.bored = False

	def __init__(self):

		# set global vars
		self.stopped = True
		self.tired = False
		self.bored = False

		# declare the coordinates of interest
		self.xLab =  -8.38
		self.yLab = -2.4
		self.xDean = -8.5
		self.yDean = -3.18
		self.xSofa = -18.7
		self.ySofa = 7.8
		self.xKitchen = -15.7
		self.yKitchen = 7.75
		self.xArun = -11.5
		self.yArun = -2.22
		self.xNadir = -19.5
		self.yNadir = 0.56
		self.goalReached = False

		# initiliaze
		rospy.init_node('map_navigation', anonymous=False)

		# perceive color blobs
		rospy.Subscriber('/blobs', Blobs, self.blobs_callback)

		# perceive bumber
		rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumper_callback)

		# # start automatic tour
		self.Speaking(-1)
		for choice in range(1, 6):
			if self.bored:
				self.playGame()
				break
			if (choice == 0):
				self.goalReached = self.moveToGoal(self.xLab, self.yLab)
				self.displayPage(choice)
				self.Speaking(choice)
			elif (choice == 1):
				self.goalReached = self.moveToGoal(self.xDean, self.yDean)
				self.displayPage(choice)
				self.Speaking(choice)
			elif (choice == 2):
				self.goalReached = self.moveToGoal(self.xArun, self.yArun)
				self.displayPage(choice)
				self.Speaking(choice)
			elif (choice == 3):
				self.goalReached = self.moveToGoal(self.xNadir, self.yNadir)
				self.displayPage(choice)
				self.Speaking(choice)
			elif (choice == 4):
				self.goalReached = self.moveToGoal(self.xSofa, self.ySofa)
				self.displayPage(choice)
				self.Speaking(choice)
			elif (choice == 5):
				self.goalReached = self.moveToGoal(self.xKitchen, self.yKitchen)
				self.displayPage(choice)
				self.Speaking(choice)

		os.system("say 'Where do you want to go now?'")
		choice = None
		while choice != 'q':

			choice = self.choose()

			if (choice == 0):
				self.goalReached = self.moveToGoal(self.xLab, self.yLab)
				self.Speaking(choice)

			elif (choice == 1):
				self.goalReached = self.moveToGoal(self.xDean, self.yDean)
				self.Speaking(choice)

			elif (choice == 2):
				self.goalReached = self.moveToGoal(self.xArun, self.yArun)
				self.Speaking(choice)

			elif (choice == 3):
				self.goalReached = self.moveToGoal(self.xNadir, self.yNadir)
				self.Speaking(choice)

			elif (choice == 4):
				self.goalReached = self.moveToGoal(self.xSofa, self.ySofa)
				self.Speaking(choice)

			elif (choice == 5):
				self.goalReached = self.moveToGoal(self.xKitchen, self.yKitchen)
				self.Speaking(choice)

			if (choice != 'q'):

				if (self.goalReached):
					rospy.loginfo("Congratulations!")

				else:
					rospy.loginfo("Hard Luck!")


	def shutdown(self):
		# stop turtlebot
		rospy.loginfo("Quit program")
		rospy.sleep()

	def moveToGoal(self, xGoal, yGoal):

		#define a client for to send goal requests to the move_base server through a SimpleActionClient
		ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

		#wait for the action server to come up
		while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
			rospy.loginfo("Waiting for the move_base action server to come up")


		goal = MoveBaseGoal()

		#set up the frame parameters
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()

		# moving towards the goal
		goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
		goal.target_pose.pose.orientation.x = 0.0
		goal.target_pose.pose.orientation.y = 0.0
		goal.target_pose.pose.orientation.z = 0.0
		goal.target_pose.pose.orientation.w = 1.0

		rospy.loginfo("Sending goal location ...")
		ac.send_goal(goal)

		ac.wait_for_result(rospy.Duration(60))

		if(ac.get_state() ==  GoalStatus.SUCCEEDED):
			rospy.loginfo("You have reached the destination")
			return True

		else:
			rospy.loginfo("The robot failed to reach the destination")
			return False

if __name__ == '__main__':
    # try:
		rospy.loginfo("You have reached the destination")
		map_navigation_gus()
		rospy.spin()

    # except:
    #   rospy.loginfo("map_navigation_gus node terminated.")
