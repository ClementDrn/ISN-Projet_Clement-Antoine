# Nom_du_Jeu

Ce jeu a été codé par **Antoine Brugger** et **Clément Darne** en Pyton 3, avec l'aide de la librairie Tkinter.

## Comment Jouer

Il suffit pour jouer d'exécuter le module *main.py*.

Voici les contrôles 

Contrôles | 1er carré | 2ème carré
--------- | --------- | ----------
Saut      |     Z     |     ↑
Gauche    |     Q     |     ←
Droite    |     D     |     →

#  Gameplay

Ce jeu est de type Platformer & Puzzle. Deux joueurs controlent deux carrés et doivent atteindre une arrivée, avec des conditions de victoires potentielles, dans chaque niveau. L'élément de Gameplay a exploité est la possibilité des deux joueurs a physiquement interragir entre eux.

## Programme

### Arborescence

```
Jeu
  └─controls.py
  └─debug.py        /!\ Ne sera pas dans le programme final.
  └─graphics.py
  └─hero.py
  └─main.py
  └─stage.py
  └─window.py
  └─levels
      └─lvl0.lvl
```


### Fonctionnement global

Lorsque le module *main.py* est exécuté, d'abord la fonction **init()** dans le module *window.py* est appelée. Cela créer une instance de la classe **Root** avec comme attributs : la fenêtre et le canvas de Tkinter. Ensuite le canvas est affiché.

Puis, c'est au tour du niveau 0 (provisoire) d'être créé : la fonction **create()** de *stage.py*. Pour cela le fichier *lvlO.lvl* du dossier *levels* est ouvert et lu, ainsi les éléments du niveau qui y sont mentionnés sont créés comme des instances de leur classe respective. Ces instances sont contenues dans un dictionnaire qui est un attribut de l'instance **stageO** de la classe **Stage**. Cette dernière classe est une surclasse mère des classes comme **Ceiling**, **Floor**.

Après les personnages sont créés et mis à des coordonnées spécifiques (provisoire : en attendant un système de spawn par niveau). Tout cela en appelant la fonction **init()** du module *hero.py*

Ensuite, c'est au tour des éléments additionnels graphiques d'être créés (dans le module *graphics.py*). Il y a pour l'instant l'objet **hTransparency**, un rectangle (rouge pour l'instant) qui vient s'afficher quand les personnages se superposent.

A ce moment les entrées possibles par les utilisateurs sont créés.

Finalement, les méthodes **move()** de **hero1** et **hero2** sont appelées. Elles permettent de calculer les prochaines coordonnées des personnages en prenant compte des commandes entrées par les joueurs et des interactions de l'environnement en jeu. Ces méthodes sont appelées de nouveau au bout de 10ms.

## Crédits

Antoine Brugger et Clément Darne
