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
Au cours de ce projet, nous souhaitons avoir une vision sur les parties que nous traitons l'un l'autre. Nous allons donc nous informer des différentes avancées au fil de celui-ci.

Configuration de la connexion au fetch :
==
Ouvrir le bashrc :  
cd ~/.bashrc  
Copier les lignes suivantes en fin de fichier :  
export ROS_MASTER_URI=http://freight100.local:11311  
export ROS_IP=<my_address_ip>  

Ouvrir ensuite le fichier hosts :  
sudo nano /etc/hosts  
Ajouter l'invité correspondant au robot via la ligne suivante :   
10.1.16.68	freight100  




