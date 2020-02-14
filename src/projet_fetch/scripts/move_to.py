#!/usr/bin/python2.7
import math, rospy
import tf
from math import atan2, sqrt, degrees
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import PoseStamped, Twist, PointStamped
from sensor_msgs.msg import Imu
from tf2_msgs.msg import TFMessage
from sensor_msgs.msg import LaserScan

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

_trans = tf.TransformListener()

goal_stamped = PoseStamped()
goal_stamped.pose.position.x = 4
goal_stamped.pose.position.y = 0
goal = [goal_stamped.pose.position.x,goal_stamped.pose.position.y]
goal_reached = False 
first_orientation = True
rospy.set_param("cmd_vel_init", [0.1,0.3])
rospy.set_param("cmd_vel_acual", [0.1,0.3])
rospy.set_param('angle_to_add', 0)

# Initialize node parrameters (parrameter name, default value)
def node_parameter(name, default):
    value= default
    try:
        value= rospy.get_param('~' + name)
    except KeyError:
        value= default
    return value

_cmd_frame_id= node_parameter('cmd_frame_id', 'base_link')

#Fonction de gestion du deplacement du robot
def movement_manager(data):
	global goal
	global goal_reached 
	vel_msg = Twist()
	pt_goal_base_link = point_goal_in_base_link(goal) 
	dist = sqrt(pt_goal_base_link.point.x**2 + pt_goal_base_link.point.y**2)
	print(" Aim point distance : " + str(dist))
	angle_to_reach, orientation_done = aim_angle_to_reach(pt_goal_base_link)
	rospy.set_param("orientation_done", orientation_done)
	#print (pt_goal_base_link)
	print(" ")
	print("Angle to reach : " + str(angle_to_reach))
	print("vel_msg.linear.x : " + str(vel_msg.linear.x) + " vel_msg.angular : " + str(vel_msg.angular.z))
	angle_to_reach = angle_correction_for_local_avoid(angle_to_reach)
	#Orientation vers le point objectif 
	orientation(angle_to_reach, vel_msg) 

	#Deplacement jusqu'a l objectif
	move_forward(pt_goal_base_link, vel_msg, orientation_done, dist)
	print("vel_msg.linear.x : " + str(vel_msg.linear.x) + " vel_msg.angular : " + str(vel_msg.angular.z))

	#Correction de vitesse lors de l approche d un obstacle	
	velocity_correction_for_local_avoid(vel_msg)
	print("AFTER CORRECT AVOID vel_msg.linear.x : " + str(vel_msg.linear.x) + " vel_msg.angular : " + str(vel_msg.angular.z))	

	#Correction de vitesse en approche de l objectif afin de ne pas tourner autour 
	goal_linear_velocity_correction(vel_msg, dist)
	print("AFTER CORRECT DIST vel_msg.linear.x : " + str(vel_msg.linear.x) + " vel_msg.angular : " + str(vel_msg.angular.z))
	#Publication de la commande de vitesse 
	_cmd_pub.publish(vel_msg)
	
def angle_correction_for_local_avoid(angle_to_reach): 
	if rospy.has_param('angle_to_add') or not first_orientation : 
		angle_to_reach = angle_to_reach + rospy.get_param('angle_to_add')
	return(angle_to_reach)


def velocity_correction_for_local_avoid( vel_msg):
	global first_orientation
	if rospy.has_param('cmd_vel_correction') and not first_orientation : 
		vel_msg.linear.x = vel_msg.linear.x*rospy.get_param("cmd_vel_correction")[0]
		vel_msg.angular.z = vel_msg.angular.z*rospy.get_param("cmd_vel_correction")[1]

def goal_linear_velocity_correction(vel_msg, dist):
	if dist < 0.3  : 
		vel_msg.linear.x = vel_msg.linear.x * dist * 3
		print("Correction approche point final : " + str(vel_msg.linear.x))
	
	

def point_goal_in_base_link(goal):
	_pt_odom = PointStamped()
	_pt_odom.header.frame_id = "odom"
	_pt_odom.point.x = goal[0]
	_pt_odom.point.y = goal[1]
	_pt_odom.point.z = 0
	
	return(_trans.transformPoint( _cmd_frame_id, _pt_odom))
	


def aim_angle_to_reach(pt_goal_base_link):
	goal_angle=[0,0]
	goal_angle[0] = pt_goal_base_link.point.x
	goal_angle[1] = pt_goal_base_link.point.y
	global posxy
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
	return (aim_angle, orientation_done) 



def orientation(angle_to_reach, vel_msg):
	global goal_reached
	if not goal_reached :
		if angle_to_reach < 0 :
			vel_msg.angular.z = -rospy.get_param("cmd_vel_init")[1]
		else : 
			vel_msg.angular.z = rospy.get_param("cmd_vel_init")[1]
	

def move_forward(pt_goal_base_link, vel_msg, orientation_done, dist):
	global goal_reached
	global first_orientation
	if orientation_done or not first_orientation : 
		first_orientation = False
		if dist > 0.05 : 
			vel_msg.linear.x = rospy.get_param("cmd_vel_init")[0]
		else : 
			goal_reached = True 
		

if __name__ == '__main__':
	print("Start move.py")	

	# Initialize command publisher:
	_cmd_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)

	#rospy.Subscriber("/tf", TFMessage, get_pose_frame_in_odom)

	rospy.Subscriber("/mobile_base/sensors/imu_data", Imu, movement_manager)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
