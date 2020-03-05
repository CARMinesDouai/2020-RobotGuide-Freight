### Projet : Robot d'acceuil 

### Developpeurs : Arthur Josi - Thibaut Desfachelles 

### Encadrants : L.Fabresse - N.Bouraqadi - G.Lozenguez

Description du projet
==
L'objectif de ce projet est de travailler avec un robot et d'en faire un robot d'acceuil.  

Les objectifs de fonctionnement du robot à l'aboutissement du projet sont les suivants :  

- Un utilisateur doit pouvoir selectionner le bureau de la personne qu'il veut rejoindre sur une interface graphique (Sur une tablette par exemple).  
- Le robot doit accompagner la personne au bureau demandé. Il doit donc prendre le chemin le plus efficace et s'arrêter une fois arrivé.  
- Au cours du trajet, le robot doit être capable d'éviter des objets imprévus à l'origine (Comme une personne ou un carton par exemple).  
- Des capteur doivent permettre d'indiquer la présence de la personne supposée le suivre. Effectivement, le robot doit s'arrêter si la personne ne suit plus (Si elle s'arrête pour discutter avec une autre personne par exemple). Dans l'idéal, il faudrait reconnaître la personne et pas uniquement une personne.  
- Le robot doit éventuellement être capable de suivre une personne dans le batîment.  

Ces objectifs de fonctionnement décomposent donc le projet en trois grandes parties :  

- La brique de déplacement réactive du robot permettant d'aller d'un bureau à un autre  
- La brique de vision du robot permettant de s'assurer le suivi de la personne interessée ou de suivre cette personne dans le bâtiment.  
- La brique d'interaction avec l'utilisateur permettant donc à celui-ci de choisir le bureau de la personne qu'il veut rejoindre.  

Répartission du travail
==
Au cours de ce projet, nous souhaitions avoir une certaine vision sur les parties que nous avons traitées l'un l'autre. Nous nous sommes donc tenus informé des avancées des deux côtés afin de pouvoir confirmer une voie de travail ou simplement débloquer l'avancée sur une partie.  
Globalement, les parties ont tout de même été réalisées individuellement de la façon suivante :  
- Thibaut Desfachelles : Partie vision - Suivi et tracking  
- Arthur Josi : Partie déplacement - Partie web  

Présentation du travail
==

### Prise en main du robot fetch 

Les premiers jours de ce projets, nous nous sommes penchés sur l'utilisation du robot fetch. Nous avons d'abord cherché à accéder au données des nodes déjà en place sur le robot depuis un pc extèrieur.  
Nous avons réussi à configurer un pc pour l'accès aux données des nodes du robot fetch (voir annexes).
Nous avons dès lors mis en place un algorithme afin de faire le mapping du bâtiment. Cependant, bien que celui-ci fût fonctionnel, des problèmes de batteries nous ont amenés à travailler à partir d'un turtlebot. Tout le travail a été effectué avec le turtlebot.  

### Travail sur le déplacement du robot

**Implémentations chronologiques**  
L'objectif étant de joindre les nodes les uns aux autres afin d'obtenir le résultat souhaité, voici ce qui a été réalisé :  
- Déplacement du robot d'un point A vers un point B (orientation et avancée) sans aucun obstacles.
- Déplacement du robot d'un point A vers un point B avec évitement d'obstacles locaux (Boîtes/personnes). Gestion de l'environnement proche à partir des données du lidar.  
- Ecriture d'un algorithme de dijkstra afin de determiner le chemin le plus court entre différents points. L'idée à l'origine était de placer des points clés dans le batîment (et ce manuellement, codés en dur) afin que le calcul du chemin le plus court soit fait à partir de la position du robot et de ces différents points.  
Du fait de la non adaptabilité et de la chronophagie dans la mise en place des points clés pour l'algorithme précédent, une autre voie à été explorée.  
- Récupération du move_base du turtlebot afin d'en extraire le path planner global. Suppression des algorithmes de déplacement et de path planner local de cette brique.  
- Récupération d'une carte du batîment et déplacement dans celui-ci via RVIZ avec avec nôtre algorithme de déplacement et le path planner éxtrait.  
- Positionnement automatique du robot dès l'ouverture de la carte dans rviz via les coordonnées choisies dans le script.  
- 


####
