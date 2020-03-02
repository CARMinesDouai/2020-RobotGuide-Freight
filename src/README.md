### Projet : Robot d'acceuil 

### Developpeurs : Arthur Josi - Thibaut Desfachelles 

Description du projet :
==
L'objectif de ce projet est de travailler avec un robot et d'en faire un robot d'acceuil.  

Le fonctionnement du robot à l'aboutissement du projet est donc le suivant :  

- Un utilisateur doit pouvoir selectionner le bureau de la personne qu'il veut rejoindre sur une interface graphique (Sur une tablette par exemple).  
- Le robot doit accompagner la personne au bureau demandé. Il doit donc prendre le chemin le plus efficace et s'arrêter une fois arrivé.  
- Au cours du trajet, le robot doit être capable d'éviter des objets imprévus à l'origine (Comme une personne ou un carton par exemple).  
- Des capteur doivent permettre d'indiquer la présence de la personne supposée le suivre. Effectivement, le robot doit s'arrêter si la personne ne suit plus (Si elle s'arrête pour discutter avec une autre personne par exemple.)
- Le robot doit éventuellement être capable de suivre une personne dans le batîment.

Ces objectifs de fonctionnement décomposent donc le projet en trois grandes parties :  
- La brique de déplacement réactive du robot permettant d'aller d'un bureau à un autre  
- La brique de vision du robot permettant de s'assurer le suivi de la personne interessée ou de suivre cette personne dans le bâtiment.  
- La brique d'interaction avec l'utilisateur permettant donc à celui-ci de choisir le bureau de la personne qu'il veut rejoindre.  

Répartission du travail : 
==
Au cours de ce projet, nous souhaitons avoir une certaine vision sur les parties que nous traitons l'un l'autre. Nous allons donc nous informer des différentes avancées tout au long de celui-ci.  
Pour le moment :  
Thibaut Desfachelles : Partie vision - Suivi et tracking  
Arthur JOSI : Partie déplacement - Partie web 

Configuration de l'environnement :
==

**Prérequis d'utilisation :**  
Il est nécéssaire d'être sous kinetic pour le bon fonctionnement des parties à suivre.  
Le tutoriel pour le Turtlebot Bringup doit avoir été complété.   

**Configuration du bashrc :**  
Ouverture du fichier :  
```cd ~/.bashrc```  
Ajout de cette ligne en fin de fichier :  
```source $HOME/catkin_ws/devel/setup.bash``` 

**Installer le nécessaire pour la partie web**  
 ```sudo apt install ros-kinetic-rosbridge-server ros-kinetic-robot-pose-publisher```  
 ```sudo apt install nodejs-legacy```  
 ```sudo apt install ros-kinetic-web-video-server```  

**Installation du projet :**  
```cd <catkin_repo>/src```  
*Attention à la ligne suivante, il faudra uniquement y mettre ce qui est éxistant dans 2020-robot-guide/src (voir pour la création d'un ZIP ou juste faire une commande pour lier le dossier au bon endroit)*  
```git clone https://github.com/CARMinesDouai/2020-RobotGuide-Freight.git```  


#### A mettre dans les annexes
- Ouvrir le fichier bashrc :  
    ```cd ~/.bashrc```  
- Copier les lignes suivantes en fin de fichier :  
    ```export ROS_MASTER_URI=http://freight100.local:11311```  
    ```export ROS_IP=<my_address_ip>```  

- Ouvrir ensuite le fichier hosts :  
    ```sudo nano /etc/hosts```  
- Ajouter l'invité correspondant au robot :   
    ```10.1.16.68	freight100```  

Les launch files et leur utilisation  
==

## Gestion des bureaux présents dans le bâtiment via console 
**Commande de lancement**  
Par défaut, la map "Lahure.yaml" est ouverte :  
``` roslaunch projet_fetch desktop_manager.launch```  

Pour utiliser une autre map : 
- Placer celle-ci dans le dossier "map" du package "Projet_fetch"  
- Utiliser la commande suivante :  
```roslaunch projet_fetch desktop_manager.launch map_name:="<map name>"```  

**Utilisation**  
La node desktop_manager demande à l'utilisateur ce qu'il souhaite faire. Trois options s'offrent à lui :   
  1- Créer/ Recréer la liste des bureaux disponibles dans le bâtiment.   
  2- Ajouter un bureau à la liste des bureaux disponibles.   
  3- Supprimer un bureau de la liste existante.  
La gestion se fait pour le moment dans la console, les commandes à entrer sont indiquées (Sauf pour quitter où la commande CTRL + C est necessaire) :

![Console_desktop_manager](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/desktop_manager.png)  

**Visualisation des bureaux**  
Lors de l'ajout d'un bureau, celui-ci s'affiche dans RVIZ à sa position.  
Lors de la supression de l'un d'eux, l'affichage est pour le moment encore là tant qu'il n'y a pas redémarrage de la node.  

![RVIZ_desktop_marker](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/Rviz_desktop_marker.png)  

## Création de la carte du bâtiment à mapper 
**Commande de lancement**  
``` roslaunch projet_fetch mapping.launch```  

**Utilisation**  
Une fois la commande lancée, il suffit de déplacer le robot dans l'environnement à mapper avec les touches du clavier.  
Quand la carte est complète, l'enregistrement de celle-ci est possible via la commande suivante qui l'enregistre dans le dossier ouvert :  
``` rosrun map_server map_saver <map_name>```

**Visualisation**  
La visualisation de la map en création est possible directement dans Rviz, déjà ouvert avec la commande de lancement.   

![Mapping_rviz](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/mapping.png) 


## Déplacement du robot vers un point objectif depuis RVIZ
**Commande de lancement**  
Sans évitement d'obstacles locaux :  
```roslaunch move_to.launch avoid:="false" web_app:="false"```  

Avec évitement d'obstacles locaux :  
```roslaunch move_to.launch avoid:="true" web_app:="false"```  

**Utilisation**  
Le départ du robot se fait toujours à la position où il apparait sur rviz et selon la même orientation.  
A noter que sa position et son orientation est modifiable.  
Une fois la commande roslaunch faite, il ne reste qu'a envoyer des *2D Nav Goal* depuis l'interface RVIZ.  

![2D_navGoal](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/2D_navGoal.png)  
![Path_planner](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/Path_planner.png) 

## Application web 
**Commande de lancement**  
Web app et déplacement du robot sans évitement d'obstacles locaux :  
``` roslaunch projet_fetch move_to.launch avoid:="false" web_app:="true"```  
Web app et déplacement du robot avec évitement d'obstacles locaux :  
``` roslaunch projet_fetch move_to.launch avoid:="true" web_app:="true"```  

**Utilisation**  
Ouverture du navigateur avec l'url correspondant à l'adresse ip du lanceur :  
```http://<robot ip>:8080```  
Selection du bureau à rejoindre via l'un des différents bouttons affichés à l'écran comme ci dessous :  

![Bureaux joignables](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/desktop_web.png)  

Possibilité de suppression des bureaux éxistants directement depuis l'interface web.

Fonctionnement des launch files via rqt_graph
==

## La gestion de bureaux objectifs 
  
**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/desktop_data_rqt.png)  

**Explications :**  
La node "desktop_manager" est la node permettant l'échange avec l'utilisateur.  
Lors de l'ajout de bureaux dans la base de donnée, cette node est prête à récuperer les coordonnées du bureau à ajouter qui lui sont envoyées depuis RVIZ sur le topic /clicked_point.  
Lorsque l'utilisateur veut supprimer un bureau, il rentre son nom qui est alors envoyé via le topic /desktop_name_to_suppress.  
La node Desktop_getName_and_sendCoord récupère alors le nom du bureau et publie les coordonnées correspondantes et desktop_manager va les supprimer.  

## Mapping à partir du robot turtlebot

**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/desktop_data_rqt.png)  

**Explications :**  

## Déplacement du robot 

**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/desktop_data_rqt.png)  

**Explications :**  

#### Déplacement réactif et non réactif

**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/desktop_data_rqt.png)  

**Explications :**  

## Déplacement du robot depuis l'interface web

**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/desktop_data_rqt.png)  

**Explications :**  

Description des différentes nodes :  
== 
 
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

**Piste réflexion amélioration node person_following**

Amélioration vitesse reconnaissance faciale :
- Utilisation de la neural stick : installation et utilisation de l'espace de travail OpenVino (probléme de version)
- Reflexion sur l'utilisation du multithreading afin de partager les différentes tâches ( difficile à adapter à la reconnaissance faciale)
- Evaluation de la distance de la personne, utilisation du cadre de reconnaissance et de la fonction de la librairie Pyrealsense2 ( getDistance())

Amélioration évaluation distance person_tracking:
- Utilisation de la fonction getDistance() de la librairie Pyrealsense2 mais non fonctionnel


Vidéo de présentation du projet :
==
Voies d'amélioration du projet :
==
- Gestion de la base de donnée de bureaux plus propre directement via l'interface web  
- Brique d'évitement plus réactive  
- Affichage de la carte avec le robot dessus sur l'interface web  


