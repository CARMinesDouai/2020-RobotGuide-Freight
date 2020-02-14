#!/usr/bin/python2.7
import rospy
from heapq import *
from math import sqrt
from geometry_msgs.msg import Pose 
from simple_controller.msg import path 

# Initialize ROS::node
rospy.init_node('Coordinate', anonymous=True)

#Definition du dictionnaire comprenant les coordonnees des points et leurs points adjacents
Coord_et_adjacence = {
	"0" : [[1,0],[1]],
	"1" : [[2,0],[0,2]],
	"2" : [[3,0],[1,3]],
	"3" : [[4,0],[2]]	
} 

posx =0
posy =0
graph = {}

def robot_pos(data) : 
	global posx
	global posy
	print("ROBOT POS RECEIVED")
	posx = data.position.x
	posy = data.position.y

def Graph_manager(data) : 
	global posx
	global posy
	global graph	
	print("DESKTOP NUMBER RECEIVED" )
	path_to_pub = path()
	aim_desktop = int(data.position.x)
	graph, n = Graph_creation(Coord_et_adjacence, posx, posy)
	print(graph)
	# Recuperation du path sous forme de liste avec le numero des points par lesquels passer
	paths = dijkstra(str(n), str(aim_desktop) , voisins)[1]
	# Creation de la liste qui contiendra les coordonnees des points du path
	coord_path = []
	for k in range(1,len(paths)) : 
		coord_path.append(Coord_et_adjacence[paths[k]][0])
	path_to_pub.path= coord_path

	print(path_to_pub.path)
	path_pub.publish(path_to_pub)	
	
def Graph_creation(Coord, posx, posy):
	Graph_list = []
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
		Graph_list[n][1].append(    ( sqrt((Coord[str(i)][0][0]-posx)**2 + (Coord[point_to_compare][0][1]-posy)),str(i)  )      )
			
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
	path_pub = rospy.Publisher('/path', path, queue_size= 1)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
