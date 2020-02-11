#!/usr/bin/python2.7
import math, rospy
import tf
import numpy
from math import atan2, sqrt, degrees, isnan
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import PoseStamped, Twist, PointStamped
from sensor_msgs.msg import Imu
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import LaserScan

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

first_orientation = True
laser_list = []
angle_to_add = 0
cmd_vel_to_add = Twist()

if rospy.has_param("cmd_vel_init"):
	a, b = rospy.get_param("cmd_vel_init")

# Initialize node parrameters (parrameter name, default value)
def node_parameter(name, default):
    value= default
    try:
        value= rospy.get_param('~' + name)
    except KeyError:
        value= default
    return value

_cmd_frame_id= node_parameter('cmd_frame_id', 'base_link')

def angle_to_add_function(data):
	global first_orientation 
	global angle_to_add
	global cmd_vel_to_add
	if rospy.has_param("orientation_done"):
		if rospy.get_param("orientation_done") or first_orientation  : 
			angle_avoidance_function()
	angle_decrementation()
	rospy.set_param("angle_to_add", angle_to_add)
	rospy.set_param("cmd_vel_to_add", [cmd_vel_to_add.linear.x, cmd_vel_to_add.angular.z])
	print("Angle to add : " + str(angle_to_add) )


def laser_data(msg):
	global laser_list
	laser_list = msg

def angle_avoidance_function():
	global laser_list
	global first_orientation 
	global angle_to_add
	first_orientation == False
	#Definition des constante de distances utiles : 
	left_angle_to_add, right_angle_to_add = 0, 0
	left_Object_avoid, right_Object_avoid = 0, 0
	Dmax = 0.3
	Dcenter = 1
	Dmin = 0.1
	#Recuperation des donnees laser utiles 
	Lengths = len(laser_list.ranges)
	left_laser_data = []
	right_laser_data= []
	center_laser_data = laser_list.ranges[Lengths/2]
	#Moyenne des distance gauche droite
	left_mean_obj_dist = 0 
	right_mean_obj_dist = 0 
	#Minimum de proximite a gauche et a droite
	left_min_dist = 0
	right_min_dist = 0
	for k in range(24,48):
		right_laser_data.append(laser_list.ranges[Lengths*k/96])
	for k in range(72,48,-1) : 
		left_laser_data.append(laser_list.ranges[Lengths*k/96])
	#print(str(center_laser_data))

	#Utilisation des donnees laser utiles 
	#Step 1 : Detection d'objet proche et augmentation de l'angle d'ecartement
	for k in range(24): 
		if right_laser_data[k] < Dmax and right_laser_data[k] > Dmin and not isnan(float(right_laser_data[k])) : 
			right_Object_avoid = right_Object_avoid + 1 
			#print("Right object to avoid : " + str(right_Object_avoid))
			#print("Right_laser data number : " + str(k) + " value : " + str(left_laser_data[k]))
			if angle_to_add < (k+1)*7 : 
				right_angle_to_add = (k+1)*7
				#print ("right angle to add : " + str(right_angle_to_add))
			right_mean_obj_dist = right_mean_obj_dist + right_laser_data[k]
			
		 
		if left_laser_data[k] < Dmax and left_laser_data[k] > Dmin and not isnan(float(left_laser_data[k])):
			left_Object_avoid = left_Object_avoid + 1 
			#print("Left_laser data number : " + str(k) + " value : " + str(left_laser_data[k]))
			#print("Left object to avoid" + str(left_Object_avoid))
			if angle_to_add > -(k+1)*7	:
				left_angle_to_add = -(k+1)*7	
				#print ("left angle to add  : " + str(left_angle_to_add))
			left_mean_obj_dist = left_mean_obj_dist + left_laser_data[k]
	if right_Object_avoid != 0 :
		right_mean_obj_dist = right_mean_obj_dist/right_Object_avoid
	elif left_Object_avoid != 0 : 
		left_mean_obj_dist = left_mean_obj_dist/left_Object_avoid 
	print ("Left mean : " + str(left_mean_obj_dist))
	print ("Right mean : " + str(right_mean_obj_dist))

	#Angle de correction a choisir si l'objet est centre : On observe la moyenne des distances
	if left_angle_to_add != 0 or right_angle_to_add != 0 : 
		if abs(left_angle_to_add + right_angle_to_add) < 30 and left_angle_to_add != 0 and right_angle_to_add != 0 : 
			if right_mean_obj_dist < left_mean_obj_dist :
				angle_to_add = left_angle_to_add
			elif right_mean_obj_dist < left_mean_obj_dist :
				angle_to_add = right_angle_to_add		
		else : 
			angle_to_add = left_angle_to_add + right_angle_to_add
	
	
			
	
def angle_decrementation():
	global angle_to_add
	if angle_to_add > 100 : 
		angle_to_add = angle_to_add - 1.5
	elif angle_to_add < -100 : 
		angle_to_add = angle_to_add + 1.5
	if angle_to_add > 50 and angle_to_add <= 100 : 
		angle_to_add = angle_to_add - 1.0
	elif angle_to_add >= -100 and angle_to_add < - 50 : 
		angle_to_add = angle_to_add + 1.0
	if angle_to_add > 0 and angle_to_add <= 50 : 
		angle_to_add = angle_to_add - 0.5
	elif angle_to_add >= -50 and angle_to_add < 0 : 
		angle_to_add = angle_to_add + 0.5

if __name__ == '__main__':
	print("Start move.py")	

	# Get laser data
	rospy.Subscriber('/scan', LaserScan, laser_data)

	#rospy.Subscriber("/tf", TFMessage, get_pose_frame_in_odom)

	rospy.Subscriber("/mobile_base/sensors/imu_data", Imu, angle_to_add_function)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
