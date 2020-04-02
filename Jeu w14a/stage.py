import window                           # le fichier stage.py définie les éléments d'un niveau
from os import getcwd


class Stage:
    def __init__(self, comObjs):
        self.objs = {"Common": comObjs}


    def display(self):              # /!\ Si des listes d'éléments sont rajoutées il faut ici aussi les rajoutées
        for category in self.objs:        
            for obj in self.objs[category]:
                self.objs[category][obj].display()
        print("display Stage")


class Floor(Stage):                 # class qui définie le sol
    def __init__(self, y):
        self.y = y

    def display(self):
        self.shape = get_can().create_rectangle(0, self.y, get_winW(), get_winH(), width=0, fill="#D0DCE0")


class Ceiling(Stage):               # class qui définie le plfond de la fenêtre 
    def __init__(self, y):
        self.y = y

    def display(self):
        self.shape = get_can().create_rectangle(0, 0, get_winW(), self.y, width=0, fill="#D0DCE0")


class WallLeft(Stage):                # class qui definie le mur de gauche 
    def __init__(self, x):
        self.x = x

    def display(self):
        self.shape = get_can().create_rectangle(0, 0, self.x, get_winH(), width=0, fill="#D0DCE0")


class WallRight(Stage):                 # class qui definie le mur de droite 
    def __init__(self, x):
        self.x = x

    def display(self):
        self.shape = get_can().create_rectangle(self.x, 0, get_winW(), get_winH(), width=0, fill="#D0DCE0")


# class Spawn(Stage):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y


def get_can():
    return window.root.canvas

def get_winH():
    return window.root.winH

def get_winW():
    return window.root.winW

def create(level):
    global stage0
    objs = []
    stage0 = Stage(objs)
    commonObjs = {"floor": 0, "ceiling": 0, "wallLeft": 0, "wallRight": 0}

    file = open(getcwd() + "\\levels\\lvl" + str(level) + ".lvl", "r")      # Ouvre un fichier, ex: "lvl2.lvl"

    for line in file:
        line = line.split()

        if line[0] == "floor":
            commonObjs[line[0]] = Floor(int(line[1]))
        if line[0] == "ceiling":
            commonObjs[line[0]] = Ceiling(int(line[1]))
        if line[0] == "wallLeft":
            commonObjs[line[0]] = WallLeft(int(line[1]))
        if line[0] == "wallRight":
            commonObjs[line[0]] = WallRight(int(line[1]))
        # if plateforme → append à la liste des plateformes.

    print(commonObjs)
    stage0 = Stage(commonObjs)
    file.close()                # Enlève le fichier de la mémoire
