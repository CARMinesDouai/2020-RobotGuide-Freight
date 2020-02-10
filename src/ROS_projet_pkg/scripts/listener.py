#!/usr/bin/python2.7
import math, rospy
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

rospy.init_node('autonomous_navigation', anonymous=True)


def laser_data(msg):
	Lengths = len(msg.ranges)
	#Recuperation des donnees laser en face et sur les cotes 
	range_center = msg.ranges[Lengths/2]
   	range_left= msg.ranges[Lengths*2/3]
    	range_right= msg.ranges[Lengths/3]
	print(str(range_center))
	rospy.loginfo(range_center)
if __name__ == '__main__':
	print("Start display data")	

	# Get laser data
	rospy.Subscriber('/base_scan', LaserScan, laser_data)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()



