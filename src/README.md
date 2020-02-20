**Projet : FetchRobot**  

**Developpeurs : Arthur Josi - Thibaut Desfachelles**  

Description du projet :
==
L'objectif de ce projet est de travailler avec un robot fetch et d'en faire un robot d'acceuil.  
Cet objectif décompose le projet en différentes grandes parties :  
- La brique de déplacement réactive du robot permettant d'aller d'un bureau à un autre  
- La brique de vision du robot permettant de s'assurer le suivi de la personne interessée ou de suivre cette personne dans le bâtiment.  
- La brique de conception du robot consistant en la création d'une structure permettant de porter une tablette, des caméras, un ou plusieurs ordinateurs.  
- La brique d'interaction avec l'utilisateur permettant donc à celui-ci de choisir le bureau de la personne qu'il veut rejoindre.  

Répartission du travail : 
==
Au cours de ce projet, nous souhaitons avoir une certaine vision sur les parties que nous traitons l'un l'autre. Nous allons donc nous informer des différentes avancées tout au long de celui-ci.  
Pour le moment :  
Thibaut Desfachelles : Partie vision - Suivi et tracking  
Arthur JOSI : Partie déplacement 

Configuration de la connexion au fetch :
==
- Ouvrir le fichier bashrc :  
*cd ~/.bashrc*  
- Copier les lignes suivantes en fin de fichier :  
*export ROS_MASTER_URI=http://freight100.local:11311*  
*export ROS_IP=<my_address_ip>*  

- Ouvrir ensuite le fichier hosts :  
*sudo nano /etc/hosts*  
Ajouter l'invité correspondant au robot :   
*10.1.16.68	freight100*  

Package ROS :
==
Le package Projet_fetch regroupe tous les fichiers important au bon fonctionnement du robot.

Les différentes nodes du package "Projet_fetch" :  
= 
Les nodes sont placées dans le dossier scripts du package.  

**Node : aim_and_pose_pub.py :**  

Cette node permet la publication d'un bureau objectif via le topic */aim_desktop* sous forme d'une *Pose*, il faut cependant revoir le message publié car il ne s'agit que d'un entier.  
Elle permet aussi de publier la position du robot *base_footprint* dans la base fixe */odom*. Cette position est de type *Pose* et est publiée via le topic */robot_pose*.  

**Node : Sending_path_node.py :**   

Cette node permet la determination du chemin le plus court pour que le robot puisse se déplacer d'un point A vers un point B.  
Description de son fonctionnement :  
- La configuration des points par lesquels le robot peut/doit passer se fait directement en brut dans le fichier .py.  
- Ensuite, cette node écoute la position du robot en permanance via le topic */robot_pose*.  
- Elle écoute attend qu'on lui envoie le numéro du bureau que l'on veut rejoindre via le topic */aim_desktop*  
- Enfin, elle publie sur le topic */path* et envoie un message de type *PoseArray* qui correspond à une liste de liste de *Pose* correspondants aux points par lesquels le robot doit passer.  

**Node : move_to.py**

Cette node permet le déplacement du robot d'un point A vers un point B.  
Description de son fonctionnement : 
- La node souscrit au topic "/path" dans l'attente de points objectifs à atteindre. Elle reçoit les points objectifs sous la forme de *PoseArray*.  
- Elle publie dans le topic "cmd_vel" pour envoyer des commandes de vitesse au robot.  
- La vitesse s'adapte en fonction de la distance au point.  
- La rotation est effectuée dans un premier temps quand un point du path à été atteint et qu'il faut en rejoindre un autre. 
- Rosparam pour la vitesse angulaire et lineaire. 

**Node : local_avoidance.py**

Cette node récupère les données laser et corrige la trajectoire du robot dans le cas où des objets seraient placés sur sa trajectoire. 
Description de son fonctionnement : 
- Récupération des données laser via le topic */scan* sous forme de message *LaserScan*. 
- 

**Node : person_tracking.py**

Cette node permet le suivi d'une personne par le robot à l'aide du retour de la caméra et des données laser:  

- la caméra permet la détection d'une personne.  
- la détection de personne se base sur un programme de deep learning.  
- le laser permet le contournement d'objet se trouvant sur le passage entre la personne à suivre et le robot.  
- Cette node publie sur le topic "cmd_vel" et souscrit au topic "/base_scan".  

**Node : person_following.py**

Cette node permet la reconnaissance faciale de la personne qui suit le robot:  

- Elle renvoie un message ROS constitué de 2 variables (1 bool et 1 int) donnant la présence ou non d'une personne et la distance à laquelle se trouve la personne.  
- La reconnaissance faciale est basée sur du deep learning, des modéles pre-entrainés provenant de la bibliothéque dlib sont utilisés afin de reconnaitre les visages des personnes selon la forme de leur visage.  

**La gestion de bureaux objectifs :**  
Le rqt graph ci-dessous permet de présenter le fonctionnement de la gestion de la base de donnée des bureaux et de leurs coordonnées.  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/Bureaux_data_rqt.png)
*Explications :*  
La node desktop_manager demande à l'utilisateur ce qu'il souhaite faire. Trois options s'offrent à lui :   
  1 - Créer/ Recréer la liste des bureaux disponibles dans le bâtiment.   
  2 - Ajouter un bureau à la liste des bureaux disponibles.   
  3 - Supprimer un bureau de la liste.  
  
 *Cas 1 et 2 :* Dans cette configuration, la node attend qu'un point soit publié sur RVIZ. Une fois cela fait, les coordonnées sont enregistré dans un fichier txt si l'utilisateur rentre le nom du bureau associé.   
 *Cas 3 :* Dans cette configuration, l'utilisateur envoie le nom du bureau qu'il veut supprimer. Le nom du bureau est envoyé à la node "get_and_send_desktop" qui publie alors les coordonnées coordonnées correspondantes à supprimer.  

