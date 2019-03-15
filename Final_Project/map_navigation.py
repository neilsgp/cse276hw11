
#! /usr/bin/env python

import rospy
import actionlib
import time
import os
import speech_recognition as sr
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point

class map_navigation_gus():

	def choose(self):

		choice='q'

		rospy.loginfo("|'0': Lab ")
		rospy.loginfo("|'1': Dean ")
		rospy.loginfo("|'2': Sofa ")
		rospy.loginfo("|'3': Big Data Lab ")
		rospy.loginfo("|'q': Quit ")
		rospy.loginfo("|WHERE TO GO?")
		choice = input()
		return choice


	def Speaking(self, schoice):
		if (schoice == -1):
			var = 'Hello! My name is Kobuki and I will take you in a fabulous adventure. Follow me.'
		elif (schoice == 0):
			var = 'Welcome to the Embedded Systems lab. Please go inside.'
		elif (schoice == 1):
			var = 'Here is Dean Tullsens office. Please knock on the door.'
		elif (schoice == 2):
			var = 'This is the sofa room. Take a seat, if you want.'
		elif (schoice == 3):
			var = 'Finally, welcome to the kitchen. Are you hungry?'
		elif (schoice == 4):
			var = 'Ok, time to go. Follow me!'
		os.system("say " +  var)

	def __init__(self):

		# declare the coordinates of interest
		self.xCafe =  -8.08
		self.yCafe = -0.601
		self.xOffice1 = -8.5
		self.yOffice1 = -3.18
		self.xOffice2 = -18.4
		self.yOffice2 = 7.43
		self.xOffice3 = -15.7
		self.yOffice3 = 7.75
		self.goalReached = False

		# initiliaze
		rospy.init_node('map_navigation', anonymous=False)

		# # start tour
		self.Speaking(-1)

		# # office
		# self.goalReached = self.moveToGoal(self.xOffice1, self.yOffice1)
		# self.Speaking(1)
		# time.sleep(5)
		# self.Speaking(4)

		# # sofa
		# self.goalReached = self.moveToGoal(self.xOffice2, self.yOffice2)
		# self.Speaking(2)
		# time.sleep(5)
		# self.Speaking(4)

		# # kitchen
		# self.goalReached = self.moveToGoal(self.xOffice3, self.yOffice3)
		# self.Speaking(3)
		# time.sleep(5)
		# self.Speaking(4)

		# # lab
		# self.goalReached = self.moveToGoal(self.xCafe, self.yCafe)
		# self.Speaking(0)
		# time.sleep(5)

		choice = None
		while choice != 'q':

			choice = self.choose()

			if (choice == 0):
				self.goalReached = self.moveToGoal(self.xCafe, self.yCafe)
				self.Speaking(choice)

			elif (choice == 1):
				self.goalReached = self.moveToGoal(self.xOffice1, self.yOffice1)
				self.Speaking(choice)

			elif (choice == 2):
				self.goalReached = self.moveToGoal(self.xOffice2, self.yOffice2)
				self.Speaking(choice)

			elif (choice == 3):
				self.goalReached = self.moveToGoal(self.xOffice3, self.yOffice3)
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
    try:
			rospy.loginfo("You have reached the destination")
			map_navigation_gus()
			rospy.spin()

    except:
      rospy.loginfo("map_navigation_gus node terminated.")
