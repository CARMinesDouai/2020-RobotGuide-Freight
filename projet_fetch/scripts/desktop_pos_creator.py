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



def desktop_pose(data) :
	desktop_coord=[0,0]
	desktop_coord[0] = data.point.x
	desktop_coord[1] = data.point.y
	#y = input("Rewrite (1), Add (2), Suppress (3)") 
	if y == 1 :
		rewrite(desktop_coord)
	if y == 2 :
		Add(desktop_coord)
	print("Waiting for an other publish point on RVIZ")
		

def rewrite(desktop_coord):
	global first_point
	desktop_coord = gestions_chiffres_significatifs( desktop_coord )
	#y = input("Rewrite (1), Add (2), Suppress (3)")
	x = input("Entrer le nom du bureau correspondant entre deux guillemet : ")
	if first_point :
		first_point = False
		fichier = open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "w")
		fichier.write(str(x))
		fichier.write("\n[{},{}]".format(desktop_coord[0],desktop_coord[1]))
		fichier.close()
	else :		
		fichier = open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "a")
		fichier.write("\n" + str(x))
		fichier.write("\n[{},{}]".format(desktop_coord[0],desktop_coord[1]))
	print("Desktop {} added".format(x))
	print("Coord added : " + str(desktop_coord))


def Add(data):
	global first_point
	string_length = ""
	desktop_coord=[0,0]
	desktop_coord[0] = data.point.x
	desktop_coord[1] = data.point.y
	desktop_coord = gestions_chiffres_significatifs( desktop_coord )
	x = input("Entrer le nom du bureau correspondant entre deux guillemet : ")	
	fichier = open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "a")
	fichier.write("\n" + str(x))
	fichier.write("\n[{},{}]".format(desktop_coord[0],desktop_coord[1]))
	print("Desktop {} added".format(x))
	print("Coord added : " + str(desktop_coord))
	print("Waiting for an other publish point on RVIZ")

def gestions_chiffres_significatifs( desktop_coord ) :
	for k in range(2):
		if desktop_coord[k] < 0 :
			#Gestion du nombre de chiffre dans le nombre recupere
			if desktop_coord[k] > -10.0 :
				string_length = str(round(desktop_coord[k],2))
				if len(string_length) < 5 : 
					desktop_coord[k] = round(desktop_coord[k],2) + 0.01
				else : 
					desktop_coord[k] = round(desktop_coord[k],2)
			elif desktop_coord[k] > -100.0 and desktop_coord[k]< -10.0 :
				string_length = str(round(desktop_coord[k],1))
				if len(string_length) < 5 : 
					desktop_coord[k] = round(desktop_coord[k],1) + 0.1
				else : 
					desktop_coord[k] = round(desktop_coord[k],1)
			else : 	
				desktop_coord[k] = round(desktop_coord[k],0)
		
		else :
			#Meme gestion pour un nombre positif 
			if desktop_coord[k] < 10.0 :
				string_length = str(round(desktop_coord[k],3))
				if len(string_length) < 5 : 
					desktop_coord[k] = round(desktop_coord[k],3) + 0.001
				else : 
					desktop_coord[k] = round(desktop_coord[k],3)
				
			elif desktop_coord[k] >= 10.0 and desktop_coord[k] < 100.0 : 
				string_length = str(round(desktop_coord[k],2))
				if len(string_length) < 5 : 
					desktop_coord[k] = round(desktop_coord[k],2) + 0.01
				else : 
					desktop_coord[k] = round(desktop_coord[k],2)
			else : 
				desktop_coord[k] = round(desktop_coord[k],1)
	return(desktop_coord)		

def suppresion() : 
	global desktop_line_to_supress
	compteur = 0
	print("Here is the list of existing desktop : " )
	with open("/home/bot/catkin_ws/src/projet_fetch/txt/desktop_list.txt", "r") as f:
	    for line in f.readlines():
		compteur = compteur + 1
		if compteur%2 == 1 : 
			print(line.strip())
	x = input("Give the name of the desktop to remove : " ) 
	desktop_line_to_supress = x
	desktop_to_remove = desktop_name()
	desktop_to_remove.desktop_name = x
	desktop_name_pub.publish(desktop_to_remove)
	

def ask_for_coord(data) : 
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
	rospy.Subscriber('/desktop_coord_to_supress', PoseStamped, ask_for_coord) 

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
