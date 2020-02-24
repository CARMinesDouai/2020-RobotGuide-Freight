#!/usr/bin/python2.7
import rospy
from heapq import *
from geometry_msgs.msg import PoseArray, PoseStamped 
from projet_fetch.msg import desktop_name, desktop_name_list
from tf2_msgs.msg import TFMessage
from visualization_msgs.msg import Marker

previous_list=[]
# Initialize ROS::node
rospy.init_node('desktop_name_list_publisher', anonymous=True)

def get_desktop_pos_list() :
	desktop_pos_list = []
	compteur = -1
	#Get all desktop coordinates 
	with open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "r") as f:
	    for line in f.readlines():
		compteur = compteur + 1
		if compteur%2==1 :
			desktop_pos_list.append([float(line.strip()[1:6]), float(line.strip()[7:12])])
	#Send a marker for each desktop 
	for k in range(len(desktop_pos_list)):
		publish_Desktop_Pos_Marker(desktop_pos_list[k][0], desktop_pos_list[k][1], k )

	

def publish_Desktop_Pos_Marker(pos_desktop_x,pos_desktop_y,id_num): 
    global ObjectCut
    rospy.loginfo(" ")
    marker_msg = Marker()

    marker_msg.header.frame_id = "map"
    marker_msg.header.stamp = rospy.Time.now()

    marker_msg.ns = "my_point"
    marker_msg.id = id_num
    #Marker color 
    marker_msg.color.r = 1.0
    marker_msg.color.g = 0.0
    marker_msg.color.b = 0.0
    marker_msg.type = Marker().CUBE
    marker_msg.action = Marker().ADD
    
    #Marker Pose
    marker_msg.pose.position.x = pos_desktop_x
    marker_msg.pose.position.y = pos_desktop_y
    marker_msg.pose.position.z = 0.0

    #Marker display 
    marker_msg.color.a = 1.0

    #Marker size
    marker_msg.scale.x = 0.15
    marker_msg.scale.y = 0.15
    marker_msg.scale.z = 0.15

    marker_msg.lifetime = rospy.Duration(0)

    desktop_pose_pub.publish(marker_msg)
		
			
if __name__ == '__main__':
	print("Start sending desktop name list")
	#Marker publisher
	desktop_pose_pub = rospy.Publisher('/desktop_pose', Marker, queue_size=10)
	
	while not rospy.is_shutdown():
		get_desktop_pos_list()
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
