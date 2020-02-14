#!/usr/bin/python2.7
import rospy
from heapq import *
from math import sqrt
from geometry_msgs.msg import PoseArray, Pose 
from projet_fetch.msg import path 
from tf2_msgs.msg import TFMessage

# Initialize ROS::node
rospy.init_node('Coordinate', anonymous=True)


first_time = True 

# Initialize node parrameters (parrameter name, default value)
def node_parameter(name, default):
    robot_pos = TFMessage()
    value= default
    try:
        value= rospy.get_param('~' + name)
    except KeyError:
        value= default
    return value

_cmd_odom_id= node_parameter('cmd_odom_id', 'odom')

def get_tf_data(data) :
	global first_time
	desktop = Pose()
	robot_pos = Pose()
	if data.transforms[0].header.frame_id == "odom"  and data.transforms[0].child_frame_id == "base_footprint" : 
		robot_pos.position.x = data.transforms[0].transform.translation.x 
		robot_pos.position.y = data.transforms[0].transform.translation.y
		robot_pos_pub.publish(robot_pos)
	print("before : " + str(first_time))
	if first_time : 
		print(first_time)	
		desktop.position.x = 2
		aim_desktop_pub.publish(desktop)
		print(desktop)
		first_time = False	
	

if __name__ == '__main__':
	print("Start sending aim and robot pose ")
	
	rospy.Subscriber('/tf', TFMessage, get_tf_data)
	
	robot_pos_pub = rospy.Publisher('/robot_pose', Pose, queue_size= 10)

	aim_desktop_pub = rospy.Publisher('/aim_desktop', Pose, queue_size= 1) 
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
