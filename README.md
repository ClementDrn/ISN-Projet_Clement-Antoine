# Projet d'ISN

Ce jeu a été codé par **Antoine Brugger** et **Clément Darne** en Python 3, avec l'aide de la librairie Tkinter.

## Installation

Tout d'abord il faut cloner le dépôt.

```bash
git clone https://github.com/ClementDrn/ISN-Projet_Clement-Antoine
```

Python 3 avec Tkinter est nécessaire pour exécuter le programme. Il peut être installé depuis le [site web officiel](https://www.python.org/downloads/).

Enfin, il faut installer les modules `pygame` et `PIL` (ou Pillow) en exécutant `install_librairies.bat`.


## Comment Jouer

Pour lancer le jeu, il suffit d'exécuter le fichier `main.py`. Vous pourrez profiter de 8 niveaux.

### Les contrôles 

Contrôles | 1er carré | 2ème carré
--------- | --------- | ----------
Saut      |     Z     |     ↑
Gauche    |     Q     |     ←
Droite    |     D     |     →

`ECHAP` permet de quitter le niveau.

### Les commandes de triche

En appuyant sur `ENTER`, le jeu est mis en pause et il devient possible de rentrer une commande dans l'invité de commandes.

Il existe plusieurs commandes :
* `help` affiche la liste des commandes.
* `finish` finit automatiquement le niveau.
* `level <number>` lance le niveau spécifié dans `<number>`.

#  Gameplay

Ce jeu est de type Platformer & Puzzle. Deux joueurs controlent deux carrés et doivent atteindre une arrivée dans chaque niveau. L'élément de Gameplay a exploité est la possibilité des deux joueurs à physiquement interragir entre eux : se porter l'un l'autre.

## Programme

### Arborescence

```
main.py
Game
  └─__init__.py
  └─controls.py
  └─debug.py
  └─graphics.py
  └─hero.py
  └─stage.py
  └─window.py
  └─music.py
  └─levels
      └─lvl1.lvl
      └─lvl2.lvl
      └─...
  └─sounds
      └─...
  └─textures
      └─...
```


### Fonctionnement global

Lorsque le module *main.py* est exécuté, d'abord la fonction **init()** dans le module *window.py* est appelée. Cela créer une instance de la classe **Root** avec comme attributs : la fenêtre et le canvas de Tkinter. Ensuite le canvas est affiché.

Puis, c'est au tour du niveau 0 (provisoire) d'être créé : la fonction **create()** de *stage.py*. Pour cela le fichier *lvlO.lvl* du dossier *levels* est ouvert et lu, ainsi les éléments du niveau qui y sont mentionnés sont créés comme des instances de leur classe respective. Ces instances sont contenues dans un dictionnaire qui est un attribut de l'instance **stageO** de la classe **Stage**. Cette dernière classe est une surclasse mère des classes comme **Ceiling**, **Floor**.

Après les personnages sont créés et mis à des coordonnées spécifiques (provisoire : en attendant un système de spawn par niveau). Tout cela en appelant la fonction **init()** du module *hero.py*

Ensuite, c'est au tour des éléments additionnels graphiques d'être créés (dans le module *graphics.py*). Il y a pour l'instant l'objet **hTransparency**, un rectangle (rouge pour l'instant) qui vient s'afficher quand les personnages se superposent.

A ce moment les entrées possibles par les utilisateurs sont créés dans *controls.py*.

Finalement, **la main_loop()** est appelée, avec dedans les méthodes **move()** de **hero1** et **hero2**. Elles permettent de calculer les prochaines coordonnées des personnages en prenant compte des commandes entrées par les joueurs et des interactions de l'environnement en jeu. La boucle principale est appelée de nouveau au bout de 10ms.

## Crédits

Antoine Brugger et Clément Darne

starfrosch pour la musique : Deadfro5h Remix Kit(c) copyright 2019 Licensed under a Creative Commons Attribution (3.0) license. http://dig.ccmixter.org/files/starfrosch/60781 
