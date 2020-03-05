#!/usr/bin/python2.7
import rospy
from heapq import *
from math import sqrt
from geometry_msgs.msg import PoseArray, Pose 
from projet_fetch.msg import path 

# Initialize ROS::node
rospy.init_node('Coordinate', anonymous=True)

# Initialize node parrameters (parrameter name, default value)
def node_parameter(name, default):
    value= default
    try:
        value= rospy.get_param('~' + name)
    except KeyError:
        value= default
    return value

_cmd_odom_id= node_parameter('cmd_odom_id', 'odom')

#Definition du dictionnaire comprenant les coordonnees des points et leurs points adjacents
Coord_et_adjacence = {
	"0" : [[0.2,0.2],[1,3]],
	"1" : [[1,0.5],[0,4]],
	"2" : [[1,0],[4]],
	"3" : [[1,1],[0,4]],
	"4" : [[2,0],[1,2,3]]	
} 

posx =0
posy =0
graph = {}

def robot_pos(data) : 
	global posx
	global posy
	posx = data.position.x
	posy = data.position.y

def Graph_manager(data) : 
	global posx
	global posy
	global graph	
	print("DESKTOP NUMBER RECEIVED" )
	#Initialize the path 
	path_to_pub = PoseArray()
	path_to_pub.poses = []
	path_to_pub.header.frame_id = _cmd_odom_id 
	
	#Get the desktop Pose Number 
	aim_desktop = int(data.position.x)

	#Creation du graph en donnant la position initiale du robot
	graph, n = Graph_creation(Coord_et_adjacence, posx, posy)
	print(graph)

	# Recuperation du path sous forme de liste avec le numero des points par lesquels passer
	paths = dijkstra(str(n), str(aim_desktop) , voisins)[1]
	
	# Creation de la liste qui contiendra les coordonnees des points du path et non leur numero uniquement
	coord_path = []
	for k in range(1,len(paths)) : 
		coord_path.append(Coord_et_adjacence[paths[k]][0])
	print(coord_path)
	# Remplissage du tableau de Pose a partir de la liste precedente
	for k in range (len(coord_path)) :
		one_pos = Pose()
		one_pos.position.x = coord_path[k][0]
		one_pos.position.y = coord_path[k][1]
		path_to_pub.poses.append(one_pos)
		print(path_to_pub.poses[k])
	#Envoie de la liste des Pose a rejoindre
	path_pub.publish(path_to_pub)	
	
def Graph_creation(Coord, posx, posy):
	Graph_list = []
	min_list = 0 
	list_dist_origin = []
	n = len(Coord)
	for k in range (n+1):
		Graph_list.append( ("{}".format(k),[]) )
	#Creation des relations entre chaque point et ceux adjacents 
	for i in range(n) : 
		# w correspond au nombre de voisins d'un point 
		w = len( Coord[str(i)][1] )
		# On calcule la distance pour chaque point voisin, et on la place dans le dictionnaire (graph_list)
		for j in range(w) :
			point_to_compare = str(Coord[str(i)][1][j])
			Graph_list[i][1].append(    ( sqrt((Coord[str(i)][0][0]-Coord[point_to_compare][0][0])**2 + (Coord[point_to_compare][0][1]-Coord[str(j)][0][1])**2),str(point_to_compare) )          )
	#Ajout des distance entre le robot et les differents autres points
	for i in range(n) :
		list_dist_origin.append(     sqrt((Coord[str(i)][0][0]-posx)**2 + (Coord[point_to_compare][0][1]-posy))   )
	min_list = list_dist_origin[0]
	min_list_pos = 0
	#Recuperation du point le plus proche du robot 
	for j in range(len(list_dist_origin)-1) :
		if min_list > list_dist_origin[j+1] : 
			min_list = list_dist_origin[j+1]
			min_list_pos = j+1

	
	Graph_list[n][1].append(    ( sqrt((Coord[str(min_list_pos)][0][0]-posx)**2 + (Coord[str(min_list_pos)][0][1]-posy)),str(min_list_pos)  )      )
			
	return(dict(Graph_list), n)


#Implementation de l'algorithme de Dijkstra en Python.

# Les arguments sont:
#  - s : le sommet source
#  - t : le sommet but
#  - voisins : fonction qui pour un sommet renvoie une liste de couples (poids, sommet) pour chaque arete sortante
# Les sommets doivent etre des objets "hachables" (nombres, chaine de caract, n-uplets...).

def dijkstra (s, t, voisins):
    M = set()
    d = {s: 0}
    p = {}
    suivants = [(0, s)] # couples (d[x],x)

    while suivants != []:

        dx, x = heappop(suivants)
        if x in M:
            continue

        M.add(x)

        for w, y in voisins(x):
            if y in M:
                continue
            dy = dx + w
            if y not in d or d[y] > dy:
                d[y] = dy
                heappush(suivants, (dy, y))
                p[y] = x

    paths = [t]
    x = t
    while x != s:
        x = p[x]
        paths.insert(0, x)

    return d[t], paths

def voisins (s):
    global graph
    return graph[s]



if __name__ == '__main__':
	print("Start sending path node")
	
	#Get the robot position in map
	rospy.Subscriber('/robot_pose', Pose, robot_pos) 
	
	#Get the aim point in data.position.x
	rospy.Subscriber('/aim_desktop', Pose, Graph_manager)

	#Publisher for different pose to reach with the robot 
	path_pub = rospy.Publisher('/path', PoseArray, queue_size= 1)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
