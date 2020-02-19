#!/usr/bin/python2.7
import rospy
import numpy
from geometry_msgs.msg import PointStamped  

first_point = True

# Initialize ROS::node
rospy.init_node('Send_goal', anonymous=True)

def desktop_pose(data) : 
	desktop_coord=[0,0]
	desktop_coord[0] = data.point.x
	desktop_coord[1] = data.point.y
	print(desktop_coord)
	write_in_text(desktop_coord)

def write_in_text(desktop_coord):
	global first_point
	x = input("Entrer le nom du bureau correspondant entre deux guillemet : ")
	print(x)	
	fichier = open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "a")
	fichier.write("\n" + str(x))
	fichier.write("\n[{},{}]".format(desktop_coord[0],desktop_coord[1]))
	print("Desktop {} added".format(x))

if __name__ == '__main__':
	print("Send goal")	
	
	#Subscriber to selected points on RVIZ
	rospy.Subscriber('/clicked_point', PointStamped, desktop_pose)

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
