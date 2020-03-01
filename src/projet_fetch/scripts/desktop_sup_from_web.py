#!/usr/bin/python2.7
import rospy
import numpy
from geometry_msgs.msg import PointStamped, PoseStamped  
from projet_fetch.msg import desktop_name 
from std_msgs.msg import String
first_point = True

# Initialize ROS::node
rospy.init_node('Desktop_manager', anonymous=True)
desktop_line_to_supress = ''	

def desktop_to_remove_listener(data) : 
	global desktop_line_to_supress
	#print("DATA RECEIVED for suppression") 
	coord_line_to_supress = "[{},{}]".format(str(data.pose.position.x),str(data.pose.position.y))
	#print("Coordinate to supress received : " + str(coord_line_to_supress))
	lines = []
	with open('/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt', 'r') as f:
		for l in f.readlines() : 
			a = str(l)
			a = a.replace('\r\n','')
			a = a.replace('\n','')
			if a != coord_line_to_supress and a != desktop_line_to_supress :
				lines.append(a)
		print("coord line to supress : " + str(coord_line_to_supress)) 
		print("desktop name line to supress : " + str(desktop_line_to_supress))
		for k in range(len(lines)):
			if k%2 == 0 :
				print(lines[k])
		#print("List of lines in txt : " + str(lines))
	with open('/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt', 'w') as f:
		f.write("\r\n".join(lines))
	print("Give the name of another desktop to remove : " )


if __name__ == '__main__':
	print("Desktop data base manager")
	print("Which option would you like ? ")
	#desktop_name_pub = rospy.Publisher('/desktop_name', desktop_name, queue_size= 10)
	desktop_name_pub = rospy.Publisher('/desktop_name_to_supress', desktop_name, queue_size= 10)
	#Subscriber to selected points on RVIZ
	#rospy.Subscriber('/move_base_simple/goal', PoseStamped, ask_for_coord)
	rospy.Subscriber('/desktop_coord_to_supress', PoseStamped, desktop_to_remove_listener) 

	while True : 
		y = input("Rewrite? (1), Add? (2), Suppress? (3)")
		if y not in [1,2,3] :
			print("Wrong value, enter another one")
		else : 
			break
	if y == 1 : 
		print("Rewrite mode selected")
		print("Waiting for published point on RVIZ")
		rospy.Subscriber('/clicked_point', PointStamped, desktop_pose)
	if y ==2 :
		print("Add desktop mode selected")
		print("Waiting for published point on RVIZ")
		rospy.Subscriber('/clicked_point', PointStamped, Add)

	if y == 3 :
		while True :
			suppresion()
			#y = input("Continue (1), Quit (2)")
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
