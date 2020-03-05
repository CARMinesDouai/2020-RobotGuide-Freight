#!/usr/bin/python2.7
import rospy
import numpy
from geometry_msgs.msg import PointStamped, PoseStamped  
from projet_fetch.msg import desktop_name, desktop
from std_msgs.msg import String
first_point = True

# Initialize ROS::node
rospy.init_node('Desktop_eraser', anonymous=True)

def desktop_to_remove_listener(data) : 
	desktop_name = data.desktop_name
	#print("DATA RECEIVED for suppression") 
	coord_line_to_supress = "[{},{}]".format(str(data.pose_x),str(data.pose_y))
	#print("Coordinate to supress received : " + str(coord_line_to_supress))
	lines = []
	with open('/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt', 'r') as f:
		for l in f.readlines() : 
			a = str(l)
			a = a.replace('\r\n','')
			a = a.replace('\n','')
			if a != coord_line_to_supress and a != desktop_name :
				lines.append(a)
		print("coord line supressed : " + str(coord_line_to_supress)) 
		print("desktop name line supressed : " + str(desktop_name))
		for k in range(len(lines)):
			if k%2 == 0 :
				print(lines[k])
		#print("List of lines in txt : " + str(lines))
	with open('/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt', 'w') as f:
		f.write("\r\n".join(lines))
	print("Give the name of another desktop to remove : " )


if __name__ == '__main__':
	#If desktop to suppress 
	rospy.Subscriber('/desktop_to_supress', desktop, desktop_to_remove_listener) 
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
