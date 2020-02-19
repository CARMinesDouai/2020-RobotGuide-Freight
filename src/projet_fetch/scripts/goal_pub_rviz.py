#!/usr/bin/python2.7
import rospy
import tf
import numpy
from geometry_msgs.msg import PoseStamped 
from move_base_msgs.msg import MoveBaseGoal
from tf2_msgs.msg import TFMessage 



# Initialize ROS::node
rospy.init_node('Send_goal', anonymous=True)

desktopA = [0,6]
desktopB = [5,4]

def coordToPoseStamped(desktop_coord) : 
	desktopA_PoseStamped = PoseStamped()
	goal_pos.header.stamp = rospy.get_rostime()
	goal_pos.header.frame_id="map"
	goal_pos.pose.position.x = desktop_coord[0]
	goal_pos.pose.position.y = desktop_coord[1]
	goal_pos.pose.orientation.z = 0.1
	
def publisher_fct(data):
	goal_pos = PoseStamped()
	goal_pos.header.stamp = rospy.get_rostime()
	goal_pos.header.frame_id="map"
	goal_pos.pose.position.x = -2.2
	goal_pos.pose.position.y = - 0.5
	goal_pos.pose.orientation.z = 0.1
	print(goal_pos)
	robot_pos_pub.publish(goal_pos)



if __name__ == '__main__':
	print("Send goal")	

	# Sending goal_pos
	robot_pos_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size= 10)
	
	#publisher_fct()
	
	rospy.Subscriber('/tf', TFMessage, publisher_fct)

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
