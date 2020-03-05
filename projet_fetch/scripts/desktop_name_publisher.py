#!/usr/bin/python2.7
import rospy
from heapq import *
from geometry_msgs.msg import PoseArray, PoseStamped 
from projet_fetch.msg import desktop_name, desktop_name_list
from tf2_msgs.msg import TFMessage
#from projet_fetch.scripts import data

previous_list=[]
# Initialize ROS::node
rospy.init_node('desktop_name_list_publisher', anonymous=True)

def get_desktop_goal() :
	desktop_name = desktop_name_list()
	#desktop_name.desktop_list[k]
	compteur = -1
	with open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "r") as f:
	    for line in f.readlines():
		compteur = compteur + 1
		if compteur%2==0 :
			desktop_name.desktop_list.append(line.strip())
			#desktop_to_reach_coord_pub.publish(desktop)
	desktop_name_pub.publish(desktop_name)
	#print(desktop_name)
		
			
if __name__ == '__main__':
	print("Start sending desktop name list")
	
	desktop_name_pub = rospy.Publisher('/desktop_name_data', desktop_name_list, queue_size= 10)
	
	while not rospy.is_shutdown():
		get_desktop_goal()
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
