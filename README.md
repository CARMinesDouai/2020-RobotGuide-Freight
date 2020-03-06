### Projet : Robot d'acceuil 

### Developpeurs : Arthur Josi - Thibaut Desfachelles 

Description du projet :
==
L'objectif de ce projet est de travailler avec un robot Turtlebot et d'en faire un robot d'acceuil.  

Les fonctionnalités sont les suivantes:  

- Un utilisateur peut selectionner le bureau de la personne qu'il veut rejoindre sur une interface web.  
- Le robot accompagne alors la personne au bureau demandé. Il prend bien entendu le chemin le plus efficace.  
- Le robot est capable d'éviter des obstacles locaux (Comme une personne ou un carton par exemple) à l'aide d'un capteur de distance à ballayage.  
- Des capteur doivent permettre d'indiquer la présence de la personne supposée le suivre. Effectivement, le robot doit s'arrêter si la personne ne suit plus (Si elle s'arrête pour discutter avec une autre personne par exemple.)  
- Une caméra réalsense permet d'indiquer la présence de la personne supposée suivre le robot. Le robot s'arrête alrs si la personne ne le suit plus (Si elle s'arrête pour discutter avec une autre personne par exemple.  

Ces objectifs de fonctionnement décomposent donc le projet en trois grandes parties :  
- La brique de déplacement réactive du robot permettant d'aller d'un bureau à un autre  
- La brique de vision du robot permettant de s'assurer le suivi de la personne interessée.  
- La brique d'interaction avec l'utilisateur permettant à celui-ci de choisir le bureau de la personne qu'il veut rejoindre.  

Installation du projet - Configuration de l'environnement
==

[Installation du projet et configuration de l'environnement](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/INSTALLATION.md)  

Lancer la démo 
==
### Commandes de lancement : 
**Démo complète sur un pc (Problème possible de performance):**   
```roslaunch projet_fetch move_to.launch avoid:="True" web_app:="True" follower:="True"```  

**Démo sur deux pc distincs (Délocalisation de la reconnaissance faciale sur un autre PC) :**     
PC 1 :  
```roslaunch projet_fetch move_to.launch avoid:="True" web_app:="True" follower:="False"```  
PC 2 :  
```roslaunch person_following person_following.launch```  

### Utilisation :
Le départ du robot se fait toujours à la [position initiale](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/tree/master/position_initiale).
Ouverture du navigateur avec l'url correspondant à l'adresse ip du lanceur :  
```http://<PC1 ip>:8080```  
Selection du bureau à rejoindre via l'un des différents bouttons de l'interface une fois la carte chargée sur la page web. A noté qu'une capture de la personne doit être faite (toujours depuis l'interface) pour le fonctionnement de la reconnaissance faciale.  

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

![Console_desktop_manager](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/Rapport_activit%C3%A9/img/desktop_manager.png)  

**Visualisation des bureaux**  
Lors de l'ajout d'un bureau, celui-ci s'affiche dans RVIZ à sa position.  
Lors de la supression de l'un d'eux, l'affichage est pour le moment encore là tant qu'il n'y a pas redémarrage de la node.  

![RVIZ_desktop_marker](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/Rapport_activit%C3%A9/img/Rviz_desktop_marker.png)  

## Création de la carte du bâtiment à mapper 
**Commande de lancement**  
``` roslaunch projet_fetch mapping.launch```  

**Utilisation**  
Une fois la commande lancée, il suffit de déplacer le robot dans l'environnement à mapper avec les touches du clavier.  
Quand la carte est complète, l'enregistrement de celle-ci est possible via la commande suivante qui l'enregistre dans le dossier ouvert :  
``` rosrun map_server map_saver <map_name>```

**Visualisation**  
La visualisation de la map en création est possible directement dans Rviz, déjà ouvert avec la commande de lancement.   

![Mapping_rviz](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/img/mapping.png) 


## Déplacement du robot vers un point objectif depuis RVIZ
**Commande de lancement**  
Sans évitement d'obstacles locaux :  
```roslaunch move_to.launch avoid:="false" web_app:="false" follower:="false"```  

Avec évitement d'obstacles locaux :  
```roslaunch move_to.launch avoid:="true" web_app:="false" follower:="false"```  

**Utilisation**  
Le départ du robot se fait toujours à la [position initiale](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/tree/master/position_initiale) où il apparait sur RVIZ et selon la même orientation.  
A noter que sa position initiale et son orientation est modifiable temporairement depuis RVIZ ou de façon permanente directement dans le launch file move_to.  
Une fois la commande roslaunch faite, il ne reste qu'a envoyer des *2D Nav Goal* depuis l'interface RVIZ.  

![2D_navGoal](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/img/2D_navGoal.png)  
![Path_planner](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/img/Path_planner.png)  

## Application web 
**Commande de lancement**  
Web app et déplacement du robot avec évitement d'obstacles locaux et reconnaissance :  
```roslaunch projet_fetch move_to.launch avoid:="true" web_app:="true" follower:="true"```  

**Utilisation**  
Ouverture du navigateur avec l'url correspondant à l'adresse ip du lanceur :  
```http://<PC ip>:8080```  
Selection du bureau à rejoindre via l'un des différents bouttons affichés à l'écran comme ci dessous :  

![Bureaux joignables](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/img/desktop_web.png)  

Fonctionnement des launch files via rqt_graph
==

## La gestion de bureaux objectifs 
  
**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/img/desktop_data_rqt.png)  

**Explications :**  
La node "desktop_manager" est la node permettant l'échange avec l'utilisateur.  
Lors de l'ajout de bureaux dans la base de donnée, cette node est prête à récuperer les coordonnées du bureau à ajouter qui lui sont envoyées depuis RVIZ sur le topic /clicked_point.  
Lorsque l'utilisateur veut supprimer un bureau, il rentre son nom qui est alors envoyé via le topic /desktop_name_to_suppress.  
La node Desktop_getName_and_sendCoord récupère alors le nom du bureau et publie les coordonnées correspondantes et desktop_manager va les supprimer.  

## Mapping à partir du robot turtlebot

**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/img/desktop_data_rqt.png)  

**Explications :**  

## Déplacement du robot 

**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/img/desktop_data_rqt.png)  

**Explications :**  

#### Déplacement réactif et non réactif

**Rqt_graph :**  

![rqt_gaph](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/src/img/desktop_data_rqt.png)  

**Explications :**  

## Déplacement du robot depuis l'interface web

Le rqt_graph a suivre correspond à celui affiché lorsque l'application est lancée et qu'un bureau à été sélectionné.

**Rqt_graph :**  

![rqt_gaph_complet](https://github.com/CARMinesDouai/2020-RobotGuide-Freight/blob/master/img/rqt_complet.png)  

**Explications :**  
Partie web : 
La page web correspond au node /rosbrige_websocket. On peut noter qu'elle reçoit la map

Description des différentes nodes :  
== 
 
Les nodes à suivre sont placées dans le dossier scripts du package projet_fetch.  

### Déplacement :  
**Node : move_to.py**  

Ce node permet le déplacement du robot d'un point A vers un point B avec des points intermédiaires.  
Il determine la distance aux points de passage du robot au fur et à mesure, il envoie les commandes vélocité, corrigée ou non selon récéption des données du node local_avoidance.py. Ces données ne sont pas envoyées depuis un topic mais sont des paramètres modifiés internes à ros (rosparam).   
Souscription : 
- Le node souscrit au topic "/move_base/DWAPlannerROS/global_plan" dans l'attente des points objectifs à atteindre. Le message reçu est de type Path.  
- Le node souscrit au topic "/new_goal" qui est un booléen. Lors de la reception de cette donnée, les paramètres sont réinitialisés et le robot s'arrête dans l'attente d'un Path.   
- Le node souscrit au topic "/emergency_stop". Lors de la reception de la donnée, les paramètres sont réinitialisés et le robot s'arrête aussi dans l'attente d'un Path.
- Le node souscrit au topic "/person_following". Un booléen est alors reçu qui permet de savoir si la personne suit le robot ou ne le suit plus.
Publication :  
- Elle publie dans le topic "/cmd_vel_mux/input/navi" pour envoyer des commandes de vitesse au robot.  

**Node : local_avoidance.py**  

Ce node récupère les données laser et modifie un rosparam qui correspond à la correction de la trajectoire du robot nécéssaire dans le cas où des objets seraient placés sur sa trajectoire.  
Le node publie aussi un message d'arrêt d'urgence lorsqu'un obstacle est quasiment au contact de celui-ci.  
Description de son fonctionnement :    
- Récupération des données laser via le topic /scan.  
- Publication sur le topic /emergency_stop.  

### WEB :  
**Node : desktop_name_publisher.py**  
Ce node permet de publier les noms des bureaux présent dans un fichier texte contant aussi les coordonnées.   
Il publie ces noms dans le topic /desktop_name_data.  Ces données sont utilisées pour le moment pour l'affichage des boutons dans la page web.

**Node : get_and_send_desktop_to_reach.py**  

Ce node souscrit au topic /desktop_to_reach_name. Lorsque le nom du bureau auquel aller est reçu, il récupère les coordonnées de celui-ci dans le fichier texte et envoie cette donnée en publiant sur le topic /move_base_simple/goal pour que le path soit calculé.  

### Gestion des bureaux :
**desktop_pos_creator.py**
Ce node permet l'échange avec l'utilisateur qui voudrait faire des modifications des bureaux éxistants (Position, Nom, Existance).  
Souscription :  
Publication :  


### Vision
**Node : person_tracking.py**  

Fonction : Suivi de personne et Reconnaissance humain
Package : Person_tracking
Node : real_time_object_detection.py

Lancer les nodes:  
Robot:  
``` rosrun turtlebot_bringup minimal.launch```  
Laser:  
``` rosrun urg_node urg_node```  
Tracking:  
``` rosrun person_tracking real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel ```  

Fonctionnement du node:  
- Le node utilise des modéles pré-entrainés provenant du deep-learning framework caffee model, il est capable de distinguer de nombreux éléments. Dans notre cas, nous le faisons reconnaître des humains.
- L'objectif de ce node est de suivre l'humain, il utilise pour cela camera realsense
- Il publie des données sur le topic /cmd_vel_mux/input/navi afin de commander le robot
- Il reçoit des données du laser et souscrit au topic /scan afin d'éviter les obstacles se plaçant entre l'humain et le robot.
- Il utilise les données renvoyées par la reconnaissance afin de situer la personne.

Pistes d'améliorations:
- Utilisation d'une camera motorisée afin de pouvoir suivre la personne en permanence et ne pas la perdre de vue.
- Amélioration de la brique réactive permettant le suivi de la personne. 

**Node : person_following.py**

Fonction : Reconnaissance Faciale  
Package : Person_following  
Node : easy_facial_recognition  

Lancer le node:   
```rosrun person_following easy_facial_recognition.py```  

Fonctionnement du node:  
- Le node utilise des modéles pré-entrainés (Deep learning) provenant de la librairie Dlib contenus dans le dossier "pretrained-models"  
- Le package contient un dossier nommé " known faces " dans lequel nous retrouvons les visages des personnes que l'on souhaite reconnaître, nous pouvons au début du programme ajouter des photos grâce à un message ROS (type projet_fetch/capture) et à l'application web.  
- Le node est aussi capable de calculer la distance à laquelle se trouve la personne grâce notamment à la fonction get_distance().  

Pistes d'améliorations:  
- Augmentation rapidité de reconnaissance grâce aux partages des calculs sur la Neural Compute Stick 2 ou de l'utilisation du Multithreading  
- Ajout de la possibilité d'une prise de photo permanente (Pour l'instant, possibilité d'ajouter une photo seulement après le lancement du programme)  
- Amélioration du calcul de distance de la personne et utilisation pour la brique de navigation move_to.py  


Vidéo de présentation du projet :
==

[Lien Vidéo](mettrelelienICI)

Voies d'amélioration du projet :
==
- Gestion de la base de donnée de bureaux plus propre directement via l'interface web  
- Brique d'évitement plus réactive  

##ANEXES 


**Node : Sending_path_node.py :**   

Cette node permet la determination du chemin le plus court pour que le robot puisse se déplacer d'un point A vers un point B.  
Description de son fonctionnement :  
- La configuration des points par lesquels le robot peut/doit passer se fait directement en brut dans le fichier .py.  
- Ensuite, cette node écoute la position du robot en permanance via le topic */robot_pose*.  
- Elle écoute attend qu'on lui envoie le numéro du bureau que l'on veut rejoindre via le topic */aim_desktop*  
- Enfin, elle publie sur le topic */path* et envoie un message de type *PoseArray* qui correspond à une liste de liste de *Pose* correspondants aux points par lesquels le robot doit passer.  


		
