#!/usr/bin/python2.7
import rospy
from heapq import *
from math import sqrt
from geometry_msgs.msg import Pose 









# Initialize ROS::node
rospy.init_node('Coordinate', anonymous=True)

#Definition du dictionnaire comprenant les coordonnees des points et leurs points adjacents
Coord_et_adjacence = {
	"0" : [[1,0],[1]],
	"1" : [[2,0],[0,2]],
	"2" : [[3,0],[1,3]],
	"3" : [[4,0],[2]]	
} 

def Graph_manager(data) : 
	pose_msg = Pose ()
	posx = data.position.x
	posy = data.position.y
	graph, n = Graph_creation(Coord_et_adjacence, posx, posy)
	# Recuperation du path sous forme de liste avec le numero des points par lesquels passer
	path = dijkstra(str(n), Point_to_reach , voisins)[1]
	# Creation de la liste qui contiendra les coordonnees des points du path
	coord_path = []
	for k in range(1, len(path)) : 
		coord_path.append(Coord_et_adjacence[path[k]])
	#Pour le moment on envoie directement la liste des coordonnees des points a parcourir dans la carte
	pose_msg.position.x = coord_path
	#pose_msg.position.y = 0 
	pose_pub.publish(pose_msg)	
	
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
		Graph_list[n][1].append(    ( sqrt((Coord[str(i)][0][0]-posx)**2 + (Coord[point_to_compare][0][1]-posy),str(n)))      )
			
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

    path = [t]
    x = t
    while x != s:
        x = p[x]
        path.insert(0, x)

    return d[t], path

def voisins (s):
    return graph[s]



if __name__ == '__main__':
	print("Start sending path node")
	get_robot_pose = rospy.Subscriber('/robot_pose', Pose, Graph_manager) 

	pose_pub = rospy.Publisher('/path', Pose, queue_size= 10)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
