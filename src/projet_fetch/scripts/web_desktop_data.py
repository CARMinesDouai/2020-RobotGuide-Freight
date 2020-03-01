#!/usr/bin/python2.7
import rospy
from heapq import *
from math import sqrt
from geometry_msgs.msg import PoseArray, PoseStamped 
from projet_fetch.msg import desktop_name, desktop 
from tf2_msgs.msg import TFMessage
#from projet_fetch.scripts import data

# Initialize ROS::node
rospy.init_node('Desktop_data', anonymous=True)

bureau_to_reach = False 
		
def get_desktop_to_suppress(data) :
	global bureau_to_reach
	#Get the desktop name to reach
	desktop_to_sup = desktop()
	desktop_to_sup.desktop_name = data.desktop_name
	compteur = 0
	#Get the desktop coordinate in a .txt file 
	with open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "r") as f:
	    for line in f.readlines():
		compteur = compteur + 1
		if compteur%2==0 :
			if bureau_to_reach :
				print("Line strip coordinate : " + line.strip())
				print(line.strip()[1:6],line.strip()[7:12])
				desktop_to_sup.pose_x, desktop.pose_y = float(line.strip()[1:6]), float(line.strip()[7:12])
				print(desktop_to_sup)
				#Publish desktop coordinates as a PoseStamped in /move_base_simple/goal, topic which calculate the shortest path
				desktop_toSupress_pub.publish(desktop_to_sup)
				bureau_to_reach = False
		else :	
			if line.strip() == desktop_to_sup.desktop_name :
				bureau_to_reach = True
				print(line.strip())
			
if __name__ == '__main__':
	print("Start sending aim and robot pose ")

	rospy.Subscriber('/desktop_name_to_supress', desktop_name, get_desktop_to_suppress)
	
	# Sending the desktop coord to supress 
	desktop_toSupress_pub = rospy.Publisher('/desktop_to_supress', desktop, queue_size= 10) 
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
