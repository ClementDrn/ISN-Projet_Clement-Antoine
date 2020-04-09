''' Voici le module qui définie les éléments d'un niveau '''

import window                           
from os import getcwd               # Pour obtenir le chemin d'accès du fichier actuel dans l'arborescence.


class Stage:
    def __init__(self, comObjs=None, otherObjs=None):
        if comObjs:                 # Pour ne pas changer ce dictionnaire quand une sous classe est créée
            self.objs = {"Common": comObjs, "Solid": otherObjs["solid"], "Semi_Solid": otherObjs["semi-solid"], 
            "Platform": otherObjs["platform"]}          # Des plateformes peuvent être à la fois dans Platform et (Semi_)Solid   
            print(self.objs)
        self.color = "#D0DCE0"


    def display(self):              # /!\ Si des listes d'éléments sont rajoutées il faut ici aussi les rajoutées
        doneObjs = []
        for category in self.objs:
            print(category)
            for key in self.objs[category]:
                obj = self.objs[category][key]
                if obj not in doneObjs:
                    print("##", category)
                    obj.display()
                    doneObjs.append(obj)
        print("display Stage")


class Floor(Stage):                 # class qui définie le sol
    def __init__(self, y):
        super().__init__()
        self.y = y

    def display(self):              # Création de la "forme" du sol (en gros la partie graphique)
        self.shape = get_can().create_rectangle(0, self.y, get_winW(), get_winH(), width=0, fill=self.color)


class Ceiling(Stage):               # class qui définie le palfond du niveau
    def __init__(self, y):
        super().__init__()
        self.y = y

    def display(self):
        self.shape = get_can().create_rectangle(0, 0, get_winW(), self.y, width=0, fill=self.color)


class WallLeft(Stage):                # class qui definie le mur de gauche 
    def __init__(self, x):
        super().__init__()
        self.x = x

    def display(self):
        self.shape = get_can().create_rectangle(0, 0, self.x, get_winH(), width=0, fill=self.color)


class WallRight(Stage):                 # class qui definie le mur de droite 
    def __init__(self, x):
        super().__init__()
        self.x = x

    def display(self):
        self.shape = get_can().create_rectangle(self.x, 0, get_winW(), get_winH(), width=0, fill=self.color)


class Block(Stage):
    def __init__(self, x, y, sX, sY):
        super().__init__()
        self.x, self.y = x, y
        self.sizeX, self.sizeY = sX, sY
        self.shape = get_can().create_rectangle(self.x, self.y,               # Création du bloc graphiquement (rectangle)
                            self.x + self.sizeX, self.y + self.sizeY,         # L'origine du rectangle est sur le sommet en haut à gauche
                            fill = self.color, width = 0)
    
    def display(self):
        self.shape = get_can().create_rectangle(self.x, self.y, 
                self.x + self.sizeX, self.y + self.sizeY, width=0, fill=self.color)


class Solid(Block):
    def __init__(self, x, y, sX, sY):
        self.state = "solid"
        super().__init__(x, y, sX, sY)


class Semi_Solid(Block):
    def __init__(self, x, y, sX, sY):
        self.state = "semi-solid"
        super().__init__(x, y, sX, sY)


class Platform():
    def __init__(self, state, x, y, sX, sY, dx, dy):
        self.block = Solid(x, y, sX, sY) if state == "solid" else Semi_Solid(x, y, sX, sY)
        self.dx, self.dy = dx, dy

    def move(self):
        self.move_update()
        get_can().move(self.block.shape, self.dx, self.dy)

    def move_update(self):
        x1, y1, x2, y2 = get_can().coords(self.block.shape)

        if x1 < 0 or x2 > get_winW():
            self.dx *= -1
        if y1 == 0 or y2 > get_winH():
            self.dy *= -1

    def display(self):
        self.block.display()
        print("+1 plateforme")
        
        

# class Spawn(Stage):                       # En cours de construction..
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y


def get_can():
    return window.root.canvas

def get_winH():
    return window.root.winH

def get_winW():
    return window.root.winW

def create(level):              # Créé le niveau demandé
    global stage0               
    objs = []                   # obs correspond aux éléments du niveau, ils seront ajoutés plus tard
    stage0 = Stage(objs)
    commonObjs = {"floor": None, "ceiling": None, "wallLeft": None, "wallRight": None}      # commonObjs c'est les éléments d'un niveau toujours présents (plus tard il y aura des éléments facultatif).
    otherObjs = {"solid": {}, "semi-solid": {}, "platform": {}}
    # A la place des 0 ils y aura des objets de la classe correspondante.

    file = open(getcwd() + "\\levels\\lvl" + str(level) + ".lvl", "r")      # Ouvre un fichier dans le dossier "levels", ex: "lvl2.lvl"

    platCount = 0

    for line in file:           # Prend chaque ligne une par une dans le fichier
        line = line.split()     # line devient une liste de "mots", le 1er est le type d'objet, la suite est ses futurs attributs.

        if line[0] == "floor":                  # On regarde quel est le premier mot, et en fonction de ce
            commonObjs[line[0]] = Floor(int(line[1]))
        if line[0] == "ceiling":
            commonObjs[line[0]] = Ceiling(int(line[1]))
        if line[0] == "wallLeft":
            commonObjs[line[0]] = WallLeft(int(line[1]))
        if line[0] == "wallRight":
            commonObjs[line[0]] = WallRight(int(line[1]))
        
        if line[0] == "platform":
            if line[1] == "solid":
                otherObjs["solid"]["platform" + str(platCount)] = Platform(line[1], int(line[2]), int(line[3]), int(line[4]), 
                                                                                    int(line[5]), int(line[6]), int(line[7]))
                otherObjs["platform"]["platform" + str(platCount)] = otherObjs["solid"]["platform" + str(platCount)]
            elif line[1] == "semi-solid":
                # otherObjs["semi-solid"].append( Platform(line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7])) )
                otherObjs["semi-solid"]["platform" + str(platCount)] = Platform(line[1], int(line[2]), int(line[3]),int(line[4]), 
                                                                                    int(line[5]), int(line[6]), int(line[7]))
                otherObjs["platform"]["platform" + str(platCount)] = otherObjs["solid"]["platform" + str(platCount)]
            platCount += 1

        # Il faudra rajouter ici d'autres élément

    stage0 = Stage(commonObjs, otherObjs)
    file.close()                # Enlève le fichier de la mémoire
