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

## Prise en main du robot fetch 

Les premiers jours de ce projets, nous nous sommes penchés sur l'utilisation du robot fetch. Nous avons d'abord cherché à accéder au données des nodes déjà en place sur le robot depuis un pc extèrieur.  
Nous avons réussi à configurer un pc pour l'accès aux données des nodes du robot fetch (voir annexes).
Nous avons dès lors mis en place un algorithme afin de faire le mapping du bâtiment. Cependant, bien que celui-ci fût fonctionnel, des problèmes de batteries nous ont amenés à travailler à partir d'un turtlebot. Tout le travail a été effectué avec le turtlebot.  

## Travail effectué pour la partie déplacement et web 

### Implémentations chronologiques    

**Déplacement :**  
- Déplacement du robot d'un point A vers un point B (orientation et déplacement) sans aucun obstacles.
- Déplacement du robot d'un point A vers un point B avec évitement d'obstacles locaux (Boîtes/personnes). Gestion de l'environnement proche à partir des données du lidar.  
- Ecriture d'un algorithme de dijkstra afin de determiner le chemin le plus court entre différents points. L'idée à l'origine était de placer des points clés dans le batîment (et ce manuellement, codés en dur) afin que le calcul du chemin le plus court soit fait à partir de la position du robot et de ces différents points.  
Du fait de la non adaptabilité et de la chronophagie dans la mise en place des points clés pour l'algorithme précédent, une autre voie à été explorée.  
- Récupération du move_base du turtlebot afin d'en extraire le path planner global. Suppression des algorithmes de déplacement et de path planner local de cette brique.  
- Récupération d'une carte du batîment et déplacement dans celui-ci via RVIZ avec avec nôtre algorithme de déplacement et le path planner global éxtrait.  

**Mise en place de l'environnement de travail :**  
- Positionnement automatique du robot dès l'ouverture de la carte dans RVIZ via les coordonnées choisies dans le script.  
- Envoie d'une coordonnée objectif depuis un node et non plus depuis RVIZ avec un 2dNavGoal. 
- Possibilité d'envoyer le robot à des coordonnées précises donc potentiellement à un bureau d'une personne. La création d'un ensemble de node permettant la gestion des coordonnées des bureaux depuis un fichier texte et RVIZ à donc été réalisé.
- Affichage de marqueurs sur RVIZ afin de visualiser les bureaux de la base de donnée. 

**Interface web utilisateur :**  
- Installation du projet existant pour l'utilisation de ROS depuis une page web.  
- Compréhension de l'utilisation des publisher et listener depuis la page web éxistante dans le projet cité précédemment et son code en Javascript/HTML.  
- Création d'un node envoyant les données des bureaux sur un topic.  
- Récupération de ces données via un listener depuis le code javascript.  
- Création de boutons sur la page web se créant dynamiquement en fonction des bureaux présent dans le fichier texte.  
- Création d'un publisher permettant d'envoyer le bureau ayant été selectionné dans la page web et association de ce publisher aux boutons.  
- Ajout d'un outil permettant la supression de la gestion des bureaux depuis l'interface web puis supression de celui-ci du fait de son obsolescence pour l'utilisateur.  
- Ajout d'un bouton permettant de stopper le robot si l'utilisateur se trompe de position.  

**Ajouts lors de la fusion de la partie vision avec le reste :**
- Création d'un bouton dans l'interface publiant un booléen pour prévenir que l'utilisateur va se prendre en photo.
- Modification du move_to pour que le robot s'arrête ou reparte en fonction de la présence ou non de l'utilisateur qui le suit.

### Travail effectué pour la partie vision

Voies d'amélioration
==

**La brique d'évitement :**   
- Il semble que certaines situations restent problématique bien qu'elles soient difficile à cerner. Peut-être faudrait-il forcer un peu plus la réorientation vers le point objectif après la correction d'évitement.  
- La visualisation des obstacles est peut être parfois un peut trop tardive.  
- Lorsque la vitesse du robot est augmentée, l'évitement peut alors poser problème. Il faudrait que les paramètres de vitesse soient configurables de façon externe au script et que les paramètres d'évitement soient calculés en fonction.  

**Le path planner :**  
- Le robot n'est pour le moment pas capable de se sortir d'une situation où la voie est bloquée de façon imprévue. L'idéal serait qu'il recalcule un autre chemin dans cette situation.  

**Page web :**  
- Dans l'idée, la gestion des bureaux et de leur base de donnée pourrait-être faite totalement depuis la page web. On peut envisager d'envoyer les points de position des bureaux par la page web en selectionnant dans la carte affichée directement et de rentrer leurs noms ensuite.



