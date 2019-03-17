
#! /usr/bin/env python

import rospy
import actionlib
import time
import os
import speech_recognition as sr
import webbrowser
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point

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
			link = 'https://neilsgp.github.io/alfred/rest.html'
		elif (schoice == 3):
			link = 'Finally, welcome to the kitchen. Are you hungry?'
		elif (schoice == 4):
			link = 'https://www.youtube.com/watch?v=p_iPD1Iv33w'
		else:
			link = 'https://google.com'

		webbrowser.open(link, new=2)

	def Speaking(self, schoice):
		if (schoice == -1):
			var = 'Hello!My name is Kobuki and I will take you in a fabulous adventure. Follow me.'
		elif (schoice == 0):
			var = 'Welcome to the Embedded Systems lab. Please go inside.'
		elif (schoice == 1):
			var = 'Here is Dean Tullsens office. Please knock on the door.'
		elif (schoice == 4):
			var = 'This is the sofa room. Take a seat, if you want.'
		elif (schoice == 5):
			var = 'Finally, welcome to the kitchen. Are you hungry?'
		elif (schoice == 6):
			var = 'Ok, time to go. Follow me!'
                elif (schoice == 2):
                        var = 'Here is Arun Kumar office'
                elif (schoice == 3):
                        var = 'Here is Nadir Weibel office'
		os.system("say " +  var)
		time.sleep(5)

	def __init__(self):

		# declare the coordinates of interest
		self.xLab =  -8.08
		self.yLab = -0.601
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
		#choice = None
		for choice in range(6):
			if (choice == 0):
				self.goalReached = self.moveToGoal(self.xLab, self.yLab)
				self.Speaking(choice)
				self.displayPage(choice)
			elif (choice == 1):
				self.goalReached = self.moveToGoal(self.xDean, self.yDean)
				self.Speaking(choice)
				self.displayPage(choice)
			elif (choice == 2):
				self.goalReached = self.moveToGoal(self.xArun, self.yArun)
				self.Speaking(choice)
				self.displayPage(choice)
			elif (choice == 3):
				self.goalReached = self.moveToGoal(self.xNadir, self.yNadir)
				self.Speaking(choice)
				self.displayPage(choice)
			elif (choice == 4):
				self.goalReached = self.moveToGoal(self.xSofa, self.ySofa)
				self.Speaking(choice)
				self.displayPage(choice)
			elif (choice == 5):
				self.goalReached = self.moveToGoal(self.xKitchen, self.yKitchen)
				self.Speaking(choice)
				self.displayPage(choice)
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

			elif (choice == 4):
				self.goalReached = self.moveToGoal(self.xSofa, self.ySofa)
				self.Speaking(choice)

			elif (choice == 5):
				self.goalReached = self.moveToGoal(self.xKitchen, self.yKitchen)
				self.Speaking(choice)
                        elif (choice == 2):
                                self.goalReached = self.moveToGoal(self.xArun, self.yArun)
                                self.Speaking(choice)
                        elif (choice == 3):
                                self.goalReached = self.moveToGoal(self.xNadir, self.yNadir)
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
