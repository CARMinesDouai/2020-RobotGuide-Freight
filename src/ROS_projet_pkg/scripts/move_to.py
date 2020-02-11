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
goal_stamped.pose.position.x = 2
goal_stamped.pose.position.y = -2
goal = [goal_stamped.pose.position.x,goal_stamped.pose.position.y]
goal_reached = False 
first_orientation = True


# Initialize node parrameters (parrameter name, default value)
def node_parameter(name, default):
    value= default
    try:
        value= rospy.get_param('~' + name)
    except KeyError:
        value= default
    return value

_cmd_frame_id= node_parameter('cmd_frame_id', 'base_link')

def movement_manager(data):
	global goal
	global goal_reached 
	vel_msg = Twist()
	pt_goal_base_link = point_goal_in_base_link(goal) 
	
	angle_to_reach, orientation_done = aim_angle_to_reach(pt_goal_base_link)
	rospy.set_param("orientation_done", orientation_done)
	#print (pt_goal_base_link)
	print("Position x : " + str(pt_goal_base_link.point.x))
	print(" ")
	#print(str(goal[0]) + " " + str(goal[1]))
	print("Angle to reach : " + str(angle_to_reach))
	
	avoidance_correction(angle_to_reach, vel_msg)

	orientation(angle_to_reach, vel_msg) 
	
	move_forward(pt_goal_base_link, vel_msg, orientation_done)
	#print(str(pt_goal_base_link))

	_cmd_pub.publish(vel_msg)
	
def avoidance_correction(angle_to_reach, vel_msg):
	rospy.set_param("cmd_vel_init", [vel_msg.linear.x,vel_msg.angular.z])
	if rospy.has_param('angle_to_add') or not first_orientation : 
		angle_to_reach = angle_to_reach + rospy.get_param('angle_to_add')

	if rospy.has_param('cmd_vel_to_add') : 
		vel_msg.linear.x = vel_msg.linear.x + rospy.get_param('cmd_vel_to_add')[0]
		vel_msg.angular.z = vel_msg.angular.z + rospy.get_param('cmd_vel_to_add')[1]


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
			vel_msg.angular.z = -0.3
		else : 
			vel_msg.angular.z = 0.3
	

def move_forward(pt_goal_base_link, vel_msg, orientation_done):
	global goal_reached
	global first_orientation
	if orientation_done or not first_orientation : 
		first_orientation = False
		dist = sqrt(pt_goal_base_link.point.x**2 + pt_goal_base_link.point.y**2)
		if dist > 0.05 : 
			vel_msg.linear.x = 0.1
		else : 
			goal_reached = True 
		print(" Aim point distance : " + str(dist))

if __name__ == '__main__':
	print("Start move.py")	

	# Initialize command publisher:
	_cmd_pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)

	#rospy.Subscriber("/tf", TFMessage, get_pose_frame_in_odom)

	rospy.Subscriber("/mobile_base/sensors/imu_data", Imu, movement_manager)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
