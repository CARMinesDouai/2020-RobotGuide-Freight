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
rospy.set_param("cmd_vel_init", [0.1,0.3])
rospy.set_param("cmd_vel_correction", [1,1])
#rospy.set_param("cmd_vel_to_add", [0,0])



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
	if rospy.has_param("orientation_done"):
		if rospy.get_param("orientation_done") or first_orientation  : 
			angle_avoidance_function()
	angle_decrementation()
	rospy.set_param("angle_to_add", angle_to_add)
	#print("Angle to add : " + str(angle_to_add) )


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
	Dmax = 0.5
	Dcenter = 1
	Dmin = 0.1
	#Recuperation des donnees laser utiles 
	Lengths = len(laser_list.ranges)
	left_laser_data = []
	right_laser_data= []
	center_laser_data = laser_list.ranges[Lengths/2]
	number_of_data_to_get = 192
	#Moyenne des distance gauche droite
	left_mean_obj_dist = 0 
	right_mean_obj_dist = 0 
	#Minimum de proximite a gauche et a droite
	left_min_dist = -1
	right_min_dist = -1
	#On prend les donnees laser a partir de 1/8 jusqu'au centre et du centre jusqu a 7/8
	for k in range(0,number_of_data_to_get/2):
		right_laser_data.append(laser_list.ranges[Lengths*k/number_of_data_to_get])
	for k in range(number_of_data_to_get-1,number_of_data_to_get/2,-1) : 
		left_laser_data.append(laser_list.ranges[Lengths*k/number_of_data_to_get])
	#last_left_laser_data = laser_list.ranges[Lengths*90/number_of_data_to_get]
	print("Last left laser data : " + str(laser_list.ranges[Lengths-1]))
	print(str(center_laser_data))

	lenght_left_list = len(left_laser_data)
	print (lenght_left_list)
	#Utilisation des donnees laser utiles 
	#Step 1 : Detection d'objet proche et augmentation de l'angle d'ecartement
	for k in range(lenght_left_list): 
		if right_laser_data[k] < Dmax and right_laser_data[k] > Dmin and not isnan(float(right_laser_data[k])) : 
			right_Object_avoid = right_Object_avoid + 1 
			#print("Right_laser data number : " + str(k) + " value : " + str(left_laser_data[k]))
			if k < 48 : 
				if angle_to_add < (k+1)*3 : 
					right_angle_to_add = (k+1)*2.5
			else : 
				if angle_to_add < 48*3 + (k-48)*1 : 
					right_angle_to_add = 48*2.5 + (k-48)*1
				print ("right angle to add : " + str(right_angle_to_add))
			right_mean_obj_dist = right_mean_obj_dist + right_laser_data[k]
			if k<lenght_left_list -1  : 
				if right_laser_data[k] < right_laser_data[k+1] and not isnan(float(right_laser_data[k+1])) : 
					right_min_dist = right_laser_data[k]
				elif right_laser_data[k] > right_laser_data[k+1] and not isnan(float(right_laser_data[k+1])) : 
					right_min_dist = right_laser_data[k+1]
		 	#print("right min distance : " + str(right_min_dist))
		if left_laser_data[k] < Dmax and left_laser_data[k] > Dmin and not isnan(float(left_laser_data[k])):
			left_Object_avoid = left_Object_avoid + 1 
			
			#print("Left_laser data number : " + str(k) + " value : " + str(left_laser_data[k]))
			if k < 48 : 
				if angle_to_add < (k+1)*3 : 
					left_angle_to_add = -(k+1)*2.5
			else : 
				if angle_to_add < 48*3 + (k-48)*1 : 
					left_angle_to_add = -48*2.5 - (k-48)*1
				print ("left angle to add  : " + str(left_angle_to_add))
			left_mean_obj_dist = left_mean_obj_dist + left_laser_data[k]
			if k< lenght_left_list - 1  : 
				if left_laser_data[k] < left_laser_data[k+1] and not isnan(float(left_laser_data[k+1])) : 
					left_min_dist = left_laser_data[k]
				elif left_laser_data[k] > left_laser_data[k+1] and not isnan(float(left_laser_data[k+1])) : 
					left_min_dist = left_laser_data[k+1]
			#print("left min distance : " + str(left_min_dist))
	if right_Object_avoid != 0 :
		right_mean_obj_dist = right_mean_obj_dist/right_Object_avoid
	if left_Object_avoid != 0 : 
		left_mean_obj_dist = left_mean_obj_dist/left_Object_avoid 

	#Angle de correction a choisir si l'objet est centre : On observe la moyenne des distances
	if left_angle_to_add != 0 or right_angle_to_add != 0 : 
		if abs(left_angle_to_add + right_angle_to_add) < 30 and left_angle_to_add != 0 and right_angle_to_add != 0 : 
			print("left mean : " + str(left_mean_obj_dist))
			print("right mean : " + str(right_mean_obj_dist))
			if right_mean_obj_dist < left_mean_obj_dist :
				print("Selection du cote de rotation gauche")
				angle_to_add = right_angle_to_add
			if right_mean_obj_dist > left_mean_obj_dist :
				print("Selection du cote de rotation droit")
				angle_to_add = left_angle_to_add		
		else : 
			angle_to_add = left_angle_to_add + right_angle_to_add
	print("Angle to add : " + str(angle_to_add) )
	ajust_velocity(left_min_dist, right_min_dist, Dmax, Dmin)
			
	
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

def ajust_velocity(left_min_dist, right_min_dist, Dmax, Dmin):
	global angle_to_add
	Int_dist = (Dmax-Dmin)/10
	#vitesse lineaire variant entre *0.2 et *1 
	Int_linear = (1.0-0.2)/10
	#vitesse angulaire variant entre *1 et *2 
	Int_angular = (2.0-1.0)/10
	test = False 
	#linear, angular = rospy.get_param("cmd_vel_actual")[0], rospy.get_param("cmd_vel_actual")[1]
	linear, angular = 0, 0 
	if rospy.has_param("cmd_vel_init"):
		for k in range(10): 
			if left_min_dist > Dmin + Int_dist*k and left_min_dist < Dmin + Int_dist*(k+1) and angle_to_add < 0 :
				test=True
				angular = (1 + Int_angular*(10-k))
				linear = 0.2 + Int_linear*k
			if right_min_dist > Dmin + Int_dist*(k) and right_min_dist < Dmin + Int_dist*(k+1) and angle_to_add > 0 :
				test=True
				angular = (1+Int_angular*(10-k))
				linear = linear = (0.2 + Int_linear*k)
		if not test : 
			linear = 1 
			angular = 1 
	print("Linear correction : " + str(linear) + " Angular correction : " + str(angular)) 
	rospy.set_param("cmd_vel_correction", [linear,angular])

if __name__ == '__main__':
	print("Start move.py")	

	# Get laser data
	rospy.Subscriber('/scan', LaserScan, laser_data)

	#rospy.Subscriber("/tf", TFMessage, get_pose_frame_in_odom)

	rospy.Subscriber("/mobile_base/sensors/imu_data", Imu, angle_to_add_function)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
