#!/usr/bin/python2.7
import rospy
from heapq import *
from geometry_msgs.msg import PoseArray, PoseStamped 
from projet_fetch.msg import desktop_name 
from tf2_msgs.msg import TFMessage
#from projet_fetch.scripts import data

# Initialize ROS::node
rospy.init_node('Desktop_getName_and_sendCoord', anonymous=True)

bureau_to_reach = False 

def get_desktop_goal(data) :
	global bureau_to_reach
	#Get the desktop name to reach
	desktop_to_reach = data.desktop_name
	#Creation of the desktop pose stamped
	desktop = PoseStamped()
	desktop.header.frame_id = "map"
	compteur = 0
	#Get the desktop coordinate in a .txt file 
	with open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "r") as f:
	    for line in f.readlines():
		compteur = compteur + 1
		if compteur%2==0 :
			if bureau_to_reach :
				print("Line strip coordinate : " + line.strip())
				print(line.strip()[1:6],line.strip()[7:12])
				desktop.pose.position.x, desktop.pose.position.y = float(line.strip()[1:6]), float(line.strip()[7:12])
				desktop.pose.orientation.w = 0.001
				print(desktop)
				#Publish desktop coordinates as a PoseStamped in /move_base_simple/goal, topic which calculate the shortest path
				desktop_to_reach_coord_pub.publish(desktop)
		else :	
			if line.strip() == desktop_to_reach :
				bureau_to_reach = True
				print(line.strip())
		
			
if __name__ == '__main__':
	print("Start sending aim and robot pose ")
	
	rospy.Subscriber('/desktop_to_reach_name', desktop_name, get_desktop_goal)
	
	# Sending goal_pos
	desktop_to_reach_coord_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size= 10)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
