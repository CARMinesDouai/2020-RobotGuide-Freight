#!/usr/bin/python2.7
import math, rospy
import tf
import time
from math import atan2, sqrt, degrees
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import PoseStamped, PoseArray, Twist, PointStamped
from sensor_msgs.msg import Imu
from nav_msgs.msg import Path
from projet_fetch.msg import new_goal, emergency

#/move_base/DWAPlannerROS/global_plan

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

_trans = tf.TransformListener()

last_goal_reached = False
first_orientation = True
rospy.set_param("cmd_vel_init", [0.2,0.3])
rospy.set_param("cmd_vel_correction", [1,1])
#Var inutile 
rospy.set_param('angle_to_add', 0)
dataFrequency = -1 
path_pos_in_odom = []
real_number_of_point_to_reach = 0 
reached_point = 0
follower_presence = True

# Initialize node parrameters (parrameter name, default value)
def node_parameter(name, default):
    value= default
    try:
        value= rospy.get_param('~' + name)
    except KeyError:
        value= default
    return value

_cmd_frame_id= node_parameter('cmd_frame_id', 'base_link')

def initialize(data):
	print("INITIALIZE CALLED")
	global last_goal_reached
	global first_orientation
	global dataFrequency
	global path_pos_in_odom
	global real_number_of_point_to_reach
	global reached_point
	last_goal_reached = False
	first_orientation = True
	dataFrequency = -1 
	path_pos_in_odom = []
	real_number_of_point_to_reach = 0 
	reached_point = 0
	rospy.set_param("cmd_vel_init", [0.2,0.3])
	#Var inutile 
	rospy.set_param('angle_to_add', 0)	

#Si un objet est trop proche du turtle, il s'arrete :
def stop_robot(data) : 
	if data.stop_all : 
		initialize(stop)

def wait_for_follower(data):
	global follower_presence
	#follower_presence = data.Presence
	
#Recuperation du path a suivre 
def getting_path(data):
	global dataFrequency
	global path_pos_in_odom
	global real_number_of_point_to_reach
	global reached_point
	dataFrequency = dataFrequency + 1
	number_of_point_to_reach = len(data.poses)
	#print("data frequency " + str(dataFrequency))
	if dataFrequency%30 == 0 : 
		real_number_of_point_to_reach = 0
		path_pos_in_odom = []
		reached_point = 0
		#print("Recuperation d'un nouveau path en cours")
		for k in range(number_of_point_to_reach):
			if k%15 == 0 and k >=40: 
				path_pos_in_odom.append([data.poses[k].pose.position.x,data.poses[k].pose.position.y])
				real_number_of_point_to_reach = real_number_of_point_to_reach + 1
		if path_pos_in_odom == [] : 
			for k in range(number_of_point_to_reach):
				if k%10 == 0 and k >=10: 
					path_pos_in_odom.append([data.poses[k].pose.position.x,data.poses[k].pose.position.y])
					real_number_of_point_to_reach = real_number_of_point_to_reach + 1
		print("New path : " + str(path_pos_in_odom))
	
	

#Fonction de gestion du deplacement du robot
def movement_manager():
	global path_pos_in_odom
	global real_number_of_point_to_reach
	global goal
	global last_goal_reached
	global reached_point
	global follower_presence
	
	if reached_point < real_number_of_point_to_reach and not last_goal_reached : 
		vel_msg = Twist()
		pt_goal_base_link = point_goal_in_base_link(reached_point) 
		print("Number of points to reach : " + str(real_number_of_point_to_reach))
		print("reached point : " + str(reached_point))
		dist = sqrt(pt_goal_base_link.point.x**2 + pt_goal_base_link.point.y**2)
		print(" Aim point distance : " + str(dist))
		angle_to_reach, orientation_done = aim_angle_to_reach(pt_goal_base_link)
		rospy.set_param("orientation_done", orientation_done)
		print(" ")
		print("Angle to reach without avoid : " + str(angle_to_reach))
		#print("vel_msg.linear.x : " + str(vel_msg.linear.x) + " vel_msg.angular : " + str(vel_msg.angular.z))
		angle_to_reach = angle_correction_for_local_avoid(angle_to_reach)
		print("Angle to reach with avoid : " + str(angle_to_reach))
		#Orientation vers le point objectif 
		orientation(angle_to_reach, vel_msg) 

		#Deplacement jusqu'a l objectif
		move_forward(pt_goal_base_link, vel_msg, orientation_done, dist)
		print("vel_msg.linear.x : " + str(vel_msg.linear.x) + " vel_msg.angular : " + str(vel_msg.angular.z))

		#Correction de vitesse lors de l approche d un obstacle	si rotation ok 
		velocity_correction_for_local_avoid(vel_msg)
		print("AFTER CORRECT AVOID vel linear : " + str(vel_msg.linear.x) + " vel angular : " + str(vel_msg.angular.z))	

		#On verifie que la personne suit bien le robot
		if follower_presence : 
			#Publication de la commande de vitesse 
			vel_pub.publish(vel_msg)
	
def angle_correction_for_local_avoid(angle_to_reach): 
	if rospy.has_param('angle_to_add') and not first_orientation : 
		angle_to_reach = angle_to_reach + rospy.get_param('angle_to_add')
	return(angle_to_reach)


def velocity_correction_for_local_avoid( vel_msg):
	global first_orientation
	if rospy.has_param('cmd_vel_correction') and not first_orientation : 
		vel_msg.linear.x = vel_msg.linear.x*rospy.get_param("cmd_vel_correction")[0]
		vel_msg.angular.z = vel_msg.angular.z*rospy.get_param("cmd_vel_correction")[1]

def point_goal_in_base_link(reached_point):
	global path_pos_in_odom
	_pt_odom = PointStamped()
	_pt_odom.header.frame_id = "odom"
	_pt_odom.point.x = path_pos_in_odom[reached_point][0]
	_pt_odom.point.y = path_pos_in_odom[reached_point][1]
	_pt_odom.point.z = 0
	return(_trans.transformPoint( _cmd_frame_id, _pt_odom))
	


def aim_angle_to_reach(pt_goal_base_link):
	goal_angle=[pt_goal_base_link.point.x, pt_goal_base_link.point.y]
	orientation_done = False 
	#Angle de rotation qu il faut dans base_footprint pour aller a l objectif
	if goal_angle[1] < 0 and goal_angle[0] < 0: 
		aim_angle = degrees(atan2(goal_angle[1], goal_angle[0])) - 180
	elif goal_angle[1] > 0 and  goal_angle[0] < 0 :
		aim_angle = 180 - degrees(atan2( goal_angle[1], goal_angle[0])) 
	else : 
		aim_angle = degrees(atan2( goal_angle[1], goal_angle[0]))
	if aim_angle < 10 and aim_angle > - 10 : 
		orientation_done = True 
		first_orientation = False
	return (aim_angle, orientation_done) 



def orientation(angle_to_reach, vel_msg):
	global last_goal_reached
	if not last_goal_reached :
		if angle_to_reach < 0 :
			vel_msg.angular.z = -rospy.get_param("cmd_vel_init")[1]
		else : 
			vel_msg.angular.z = rospy.get_param("cmd_vel_init")[1]
	
def move_forward(pt_goal_base_link, vel_msg, orientation_done, dist):
	global last_goal_reached
	global real_number_of_point_to_reach
	global first_orientation
	global reached_point
	if orientation_done or not first_orientation : 
		first_orientation = False
		if dist > 0.1 : 
			vel_msg.linear.x = rospy.get_param("cmd_vel_init")[0]
		else :  
			print("REAAAAAAAACHED")
			reached_point = reached_point + 1 
			if reached_point == real_number_of_point_to_reach :
				last_goal_reached = True 
			else : 
				vel_msg.linear.x = rospy.get_param("cmd_vel_init")[0]
			
		
def listener_global_plan(data) : 
	print(data)

if __name__ == '__main__':
	print("Start move.py")	

	# Initialize command publisher:
	vel_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)

	#Global path calculator
	rospy.Subscriber("/move_base/DWAPlannerROS/global_plan", Path, getting_path)

	#New goal from web interface -> Initialisation 
	rospy.Subscriber("/new_goal", new_goal, initialize)

	#Too close object -> STOP
	rospy.Subscriber("/emergency_stop", emergency, stop_robot)

	#Person presence behind 
	rospy.Subscriber("/follower_presence", emergency, wait_for_follower)

	
	while not rospy.is_shutdown():
		movement_manager()
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
