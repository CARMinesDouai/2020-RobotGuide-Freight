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

**Installation des librairies pour la partie vision**  
Verifiez la version de python utilisée:  
Dlib:  
```pip3 install dlib```  
OpenCV:  
```pip3 install opencv-python```  
Pillow:  
```pip3 install pillow```  
Numpy:  
```pip3 install numpy```  
Imutils:  
```pip3 install imutils```  
Argparse:  
```pip3 install argparse```  
os:  
```pip3 install os```  
rospy:  
```pip3 install rospy```  
ntpath:  
```pip3 install ntpath```  
pyrealsense2:  
```pip3 install pyrealsense2```  

**Installation du projet :**  
```cd```  
```git clone https://github.com/CARMinesDouai/2020-RobotGuide-Freight.git```  
Ajout des liens symboliques dans catkin :  
```cd <catkin_repo>/src```  
```ln -s <2020-RobotGuide-Freight>/src/person_following/```  
```ln -s <2020-RobotGuide-Freight>/src/projet_fetch/```  
```ln -s <2020-RobotGuide-Freight>/src/turtlebot_web-master/```  

**Optionel : Lancer nodes sur 2 PC distincts avec un master commun**  
Nous avons utilisé cette méthode pour lancer le node de détéction sur un autre PC et ainsi améliorer la vitesse de traîtement des données.  
 
Ouvrir le fichier bashrc:  
``` gedit ~/.bashrc```  
Ajoutez les lignes ci dessous à la fin du fichier:  
export ROS_IP=`hostname -I`  
export ROS_MASTER_URI=http://<adresse ip du master>:11311  
Ouvrir le fichier hosts:  
```sudo gedit /etc/hosts```  
Ajouter le nom du pc :  
```<adresse ip du pc distant> <nom du pc distant>```  
