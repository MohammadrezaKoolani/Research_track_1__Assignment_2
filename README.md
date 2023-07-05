# Research_Track_2__Assignment_1&2
The assignment consist of a development of a package that interact with a simulation of a simple robot in Gazebo. The package contains three nodes:
- Node A: 
A node that implements an action client, allowing the user to set a target (x, y) or to cancel it. The node
also publishes the robot position and velocity as a custom message (x,y, vel_x, vel_z), by relying on the values
published on the topic /odom. Please consider that, if you cannot implement everything in the same node, you
can also develop two different nodes, one implementing the user interface and one implementing the publisher
of the custom message. 

- Node B:
 A service node that, when called, prints the number of goals reached and cancelled.

- Node C: 
A node that subscribes to the robot’s position and velocity (using the custom message) and prints the
distance of the robot from the target and the robot’s average speed. Use a parameter to set how fast the
node publishes the information. 

- Has also been implemented a **.launch** file that starts the whole simulation and the Noe A. 


# Documentation URL
https://mohammadrezakoolani.github.io/Research_track_1__Assignment_2/



# Installing and running
The purpose of this assignment to develop a ROS package containing three ROS nodes that provide a way to interact with the environment presented in the assignment_2_2022 package. Python nodes were written for the assignment, as well as the directory and the CMakeList file were modified. A launch file was also developed for executing the code.

The simulation requires the following steps for running:

- A ROS Noetic
- Run the ROS core by executing this command in terminal:
```python
roscore

```
- Creat a ROS worksapace:
```python
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
```
- Source the new setup.*sh file:
```python
source ~/catkin_ws/devel/setup.bash

Move to the src folder of the workspace:
```python
 cd ~/catkin_ws/src   
```
```
- Clone the package assignment_2_2022 which provides an implementation of an action server that moves a robot in the environment by implementing the bug0 algorithm:
```python
git clone https://github.com/CarmineD8/assignment_2_2022
```
- Clone the package of my solution for this assignmebt:
```python
git clone https://github.com/PeymanPP5530/final_RT1_2nd_assignment
```
- And finally:
```python
cd ~/catkin_ws 
catkin_make
```
- Now, it is possible to run the whole project by running the launch file:
```python
   roslaunch Assignment_2 assignment_2.launch
```
- To call node B and node C:
```python
  rosrun Assignment_2 node_b.py
  rosrun Assignment_2 node_c.py
```
# Jupyter Code Usage

The Jupyter code file `jupyter_code.ipynb` provides a graphical interface and visualization capabilities. This README explains how to use the code and provides an overview of the included functions.

## Usage

To use the Jupyter code, follow these steps:

1. Make sure you have Jupyter installed on your system.
2. Open a terminal and navigate to the directory containing the `jupyter_code.ipynb` file.
3. Launch Jupyter Notebook by running the command: `jupyter notebook`.
4. The Jupyter Notebook interface will open in your web browser. Click on the `jupyter_code.ipynb` file to open it.
5. Execute the code cells in the notebook to see the visualization and interact with the controls.

## Functions Explanation

The Jupyter code contains the following functions:

### Visualiser Class

- `__init__(self)`: Initializes the visualizer by creating a figure and axes for the plot.
- `update_plot(self, x, y)`: Updates the plot with the current robot position `(x, y)`.
- `set_target(self, event)`: Sets a new target position for the robot based on the clicked location on the plot.
- `cancel_target(self, event)`: Cancels the current target position.
- `start_visualizer()`: Starts the visualizer by creating the plot and connecting the event handlers.
- `set_target_position(x, y)`: Sends a new target position `(x, y)` to Node A via a ROS service call.
- `cancel_target()`: Cancels the current target position by sending a cancel signal to Node A via a ROS action client.

#### VisualizerGoals Class

- __init__(self): Initializes the visualizer for goal states by creating a figure and axes for the bar chart.
- update(self, s, c): Updates the bar chart with the counts of successful and failed goals.
    - s: The number of successful goals.
    - c: The number of failed goals.

## Interacting with the Environment

To interact with the environment and control the robot, you can follow these steps:

1. Run the ROS simulation and launch the package as described in the previous section.
2. Open the Jupyter notebook jupyter_code.ipynb.
3. Execute the code cells in the notebook to initialize the visualizer and create the plot.
4. Click on the plot to set a new target position for the robot. The robot will start moving towards the clicked location.
5. To cancel the current target position, click on the plot again.
6. Repeat steps 4 and 5 to set new targets and cancel them as needed.
7. The plot will update in real-time to show the current position of the robot.
8. The bar chart will update to display the count of successful and failed goals.

Feel free to explore the code and make any necessary modifications to suit your specific requirements.


# Node A:
Initialize object Pose() and Twist()
global variable pub_info, target_reached, target_canceled, service, pub_target
	
function clbk_odom(CustomMessage: msg){
  get from msg the position and velocity of the robot
  then publish them to the custom message tag for
  robot info
  
	msg_info <- Info()
	
	msg_info.x <- msg.x
	msg_info.y <- msg.y
	msg_info.vel_x <- msg.vx
	msg_info.vel_y <- msg.vy
  
  publish(msg_info)
} 
		
function getCordinatesFromConsole(){
  print(Set a new target)
  
  while True {
    x <- print (x = )
    y <- print (y = )
    if x AND y are a proper numbers Then
      exit from the while
  }
  return x, y
}
	
function ltk_tgt(double: x,double: y){
  target <- Point()
	
	target.x <- x
	target.y <- y	
	target.z <- 0
	
	publish(target)
}
	

function get_info_goal(CustomMessage: req){
  response <- targetResponse(boudle: target_reached,double: target_canceled)
	return response
}	

main(){

	#Initialization of elements
	pose <- PoseStamped()
	double: target_reached <- 0
	double: target_canceled <- 0
	
	init node A
	
  client <- new SimpleActionClient on tag '/reaching_goal' using CustomMessage of assignment_2_2022.msg.PlanningAction

  pub_info <- new publisher on '/bot_info' that use CustomMessage Info
  pub_target <- new publisher on '/tgt' that use CustomMessage Point
	
  sub_odom <- new subscriber of '\odom' with CusmoMessage Odometry
	service <- new service of 'goal_info' with message targetwho that use a callback function = get_info_goal
	
	client.wait_for_server()
		
	while True {
		p <- getCordinatesFromConsole()
		
		ltk_tgt(p[0],p[1])
		pose.x = p[0];
		pose.y = p[1];
		pose.z = 0;
		
		goal <- create a new goal with target_pose = pose
			
		client.send_goal(goal)
				
		finished = False
    
		print(Do you wanna cancel this target ? (Y/N))
    
		while not finished {
      res <- read from commandline
				if res = 'Y' OR res = 'y' OR res = 'yes':
					finished <- True					
					client.cancel_goal()						
			else 				
				time.sleep(1)		
				state <- client.get_state()
				if(state != 1 and state != 0) Then
					print("Targhet reachedd!) 				
					finished <- True 
    		}
			  
		
		time.sleep(1)
		state = client.get_state()
		if(state = 2) Then			
			target_canceled <- target_canceled + 1
		elif(state == 3) Then			
			target_reached <- target_reached + 1
		else
			printf(Error...)
	}
}
'''
