"""
.. module:: node_b

:platform: Unix
:synopsis: Python module 

.. moduleauthor:: Mohammadreza Koolani Koolani.mohammad@gmail.com

A service node that, when called, prints the number of goals reached and cancelled.

"""
#! /usr/bin/env python3

import rospy
import actionlib
import actionlib.msg
#import Assignment_2.msg
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist, PoseStamped
#from Assignment_2.msg import Info
#import assignment_2_2022.msg
#from Assignment_2.srv import target, targetResponse

def getInfoGoal():
	"""
	Calls the 'goal_info' service and prints the target reached and target canceled counts.
	"""
	rospy.wait_for_service('goal_info')
	try:
		handle = rospy.ServiceProxy('goal_info', target)
		resp = handle()
		print("Target reached: ", resp.reached, "Target canceled: ", resp.canceled)
	except rospy.ServiceException as e:
		print("Service call failed: %s" % e)

if __name__ == "__main__":
	getInfoGoal()

