from heapq import *
from math import sqrt
#Implementation de l'algorithme de Dijkstra en Python.

# Les arguments sont:
#  - s : le sommet source
#  - t : le sommet but
#  - voisins : fonction qui pour un sommet renvoie une liste de couples (poids, sommet) pour chaque arete sortante
# Les sommets doivent etre des objets "hachables" (nombres, chaine de caract, n-uplets...).

#Definition des coordonnees des differents points avec leurs adjacences  : 


Coord_et_adjacence = {
	"0" : [[1,0],[1]],
	"1" : [[2,0],[0,2]],
	"2" : [[3,0],[1,3]],
	"3" : [[4,0],[2]]	
}

#Objectif : creation d'une liste avec [("coucou",[ (12, "B"), (13, "C") ])]  


def Graph_creation(Coord):
	Graph_list = []
	n = len(Coord)
	for k in range (n):
		Graph_list.append( ("{}".format(k),[]) )
	#Creation des relations entre chaque point et ceux adjacents 
	for i in range(n) : 
		# w correspond au nombre de voisins d'un point 
		w = len( Coord[str(i)][1] )
		# On calcule la distance pour chaque point voisin, et on la place dans le dictionnaire (graph_list)
		for j in range(w) :
			point_to_compare = str(Coord[str(i)][1][j])
			Graph_list[i][1].append(    ( sqrt((Coord[str(i)][0][0]-Coord[point_to_compare][0][0])**2 + (Coord[point_to_compare][0][1]-Coord[str(j)][0][1])**2),str(point_to_compare) )          )
	return(dict(Graph_list))

def dijkstra (s, t, voisins):
    M = set()
    d = {s: 0}
    p = {}
    suivants = [(0, s)] #Â tas de couples (d[x],x)

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


# Exemple d'utilisation avec un graphe represente par une liste d'adjacence.

graph = {
    "A": [ (1, "B") ],
    "B": [ (1, "D"), (3, "C"), (1, "A") ],
    "C": [ (1, "D"), (3, "B") ],
    "D": [ (1, "C"), (1, "B") ]
}

print(Graph_creation(Coord_et_adjacence))
graph = Graph_creation(Coord_et_adjacence)

def voisins (s):
    return graph[s]

print(dijkstra("0", "2", voisins)[1])
