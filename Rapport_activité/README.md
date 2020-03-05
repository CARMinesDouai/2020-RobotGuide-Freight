# 2020-RobotGuide-Freight

Ce projet consiste à ré-actualiser une démonstration robotique existante de robot guide dont une vidéo est disponible [ici](http://car.imt-lille-douai.fr/2014/10/controlling-robots-with-pharos/).
Le code de cette démonstration a été écrit en [PhaROS](http://car.imt-lille-douai.fr/category/software/pharos/) i.e. Pharo et ROS pour le robot Robulab et est disponible [ici](https://partage.imt.fr/index.php/s/6Ac6QQdTfS42ene).

Dans ce projet nous souhaiterions :
- Porter cette démonstration pour le robot [Freight](https://docs.fetchrobotics.com/)
- Adaptater matériellement la partie supérieure du robot avec : une ou plusieurs caméra, un écran ou une tablette, ...
- Améliorer la démonstration existante avec:
	- une détection et un suivi de la personne guidée par vision ; c'est-à-dire que le robot est capable de détecter que la personne guidée ne suit plus et s'arrête pour reprendre ensuite le trajet, ...
	- une meilleure brique de navigation plus réactive
	- ...

## Connexion au Freight

Le robot freight embarque déjà un ordinateur sous Ubuntu/ROS et lance automatiquement les noeuds pour le contrôler au démarrage.

La machine s'appelle *freight100*, elle est sur le réseau *robots* et possède un compte *bot*.

Pour s'y connecter :

```bash
ssh bot@freight100.local
```

Cependant, vous ne devriez pas avoir besoin de vous y connecter. Vos contributions tourneront sur une seconde machine communiquant avec *freight100*.

Pour se faire, il faut configurer l'environnement de travail :

```bash
# Configure Freight100 as master:
export export ROS_MASTER_URI=http://freight100.local:11311
export export ROS_HOSTNAME=`hostname`.local
```

Toute modification effectuée directement sur *freight100* devra être soigneusement consignée.
