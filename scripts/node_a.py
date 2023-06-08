"""
.. module:: node_a

:platform: Unix
:synopsis: Python module 

.. moduleauthor:: Mohammadreza Koolani Koolani.mohammad@gmail.com

A node that implements an action client, allowing the user to set a target (x, y) or to cancel it. The node also publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z), by relying on the values published on the topic /odom. Please consider that, if you cannot implement everything in the same node, you can also develop two different nodes, one implementing the user interface and one implementing the publisher of the custom message.

"""
#! /usr/bin/env python3
import sys
import rospy
import select
import actionlib
import time
import actionlib.msg
#import Assignment_2.msg
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist, PoseStamped
#from Assignment_2.msg import Info
#from Assignment_2.srv import target,targetResponse
#import assignment_2_2022.msg

#Global variables
pose_ = Pose()
twist_ = Twist()
	
def clbk_odom(msg):
	"""
	Callback function for '/odom' topic.
	Updates the position and velocity information.
	"""

	global pub_info
	
	x_ = msg.pose.pose.position.x
	y_ = msg.pose.pose.position.y
	vx_ = msg.twist.twist.linear.x
	vy_ = msg.twist.twist.linear.y

	msg_info = Info()
	
	msg_info.x = x_
	msg_info.y = y_
	msg_info.vel_x = vx_
	msg_info.vel_y = vy_
	
	if not rospy.is_shutdown():
		pub_info.publish(msg_info)
		
	
def getCordinatesFromConsole():
	"""
	Prompts the user to enter target coordinates.
	Returns the x and y values as floats.
	"""		

	print("Set a new target:")
	while True:
		try:
			x = float(input("x = "))
		except:
			print("Please enter a valid number")			
		else:
			break
	while True:
		try:
			y = float(input("y = "))
		except:
			print("Please enter a valid number")			
		else:			
			break	
	return x,y
	
def ltk_tgt(x, y):

	"""
	Publishes the target coordinates.
	"""
	global pub_target
	
	target = Point()
	
	target.x = x
	target.y = y	
	target.z = 0
	
	pub_target.publish(target)

def get_info_goal(req):
	"""
	Service callback function for 'goal_info' service.
	Returns the target reached and target canceled counts.
	"""
	global target_reached, target_canceled, service 
	
	return targetResponse(target_reached, target_canceled)
	

def main():


	"""
	Main function of node_a.
	- Initializes ROS node and necessary elements.
	- Sends goal requests to the server.
	- Handles user input for canceling the target.
	- Prints the target reached and target canceled counts.
	"""
	global pub_info, target_reached, target_canceled, service, pub_target

	#Initialization of elements
	pose = PoseStamped()
	target_reached = 0
	target_canceled = 0
	
	#Init node
	rospy.init_node('node_a')
	
	#Create a new client
	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
	
	#Publish
	pub_info = rospy.Publisher('/bot_info', Info, queue_size=1)	
	pub_target = rospy.Publisher('/tgt', Point, queue_size=1)
	
	#Subscribe to \odom
	sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)	
	service = rospy.Service('goal_info',target, get_info_goal)
	
	#Wait for the server ready
	client.wait_for_server()
		
	while True:
		p = getCordinatesFromConsole()
		
		ltk_tgt(p[0],p[1])
		pose.pose.position.x = p[0];
		pose.pose.position.y = p[1];
		pose.pose.position.z = 0;
		
		#Create the object PlanningGoal and assign the position goal
		goal = assignment_2_2022.msg.PlanningGoal(target_pose = pose)
			
		#Send the goal request
		client.send_goal(goal)
				
		finished = False
		print("Do you wanna cancel this target ? (Y/N)")
		while not finished:						
			input = select.select([sys.stdin], [], [], 1)[0]
			if input:
				res = sys.stdin.readline().rstrip()	
				if res == 'Y' or res == 'y' or res == 'yes':
					finished = True					
					client.cancel_goal()						
			else:
				#Check of the state 	
				time.sleep(1)		
				state = client.get_state()
				if(state != 1 and state != 0):
					print("Targhet reachedd!") 				
					finished = True 
		
		time.sleep(1)
		state = client.get_state()
		if(state == 2):
			#Preempted task
			target_canceled = target_canceled + 1
		elif(state == 3):
			#Task completed
			target_reached = target_reached + 1
		else:
			printf("Error...")
		
		print("Target R: ",target_reached," C: ",target_canceled)		
		
if __name__ == "__main__":
    main()
