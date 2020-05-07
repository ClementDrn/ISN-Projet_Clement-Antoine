''' Voici le module qui définie les éléments d'un niveau '''

import window                           
from os import getcwd               # Pour obtenir le chemin d'accès du fichier actuel dans l'arborescence.


class Stage:
    def __init__(self, comObjs=None, otherObjs=None):
        if comObjs:                 # Pour ne pas changer ce dictionnaire quand une sous classe est créée
            self.objs = {"Common": comObjs, "Solid": otherObjs["solid"], "Semi_Solid": otherObjs["semi-solid"], 
            "Platform": otherObjs["platform"], "Block": otherObjs["block"]}          # Des plateformes peuvent être à la fois dans Platform et (Semi_)Solid   
            print(self.objs)
        self.color = "#D0DCE0"
        self.chunks = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    def display(self):              # /!\ Si des listes d'éléments sont rajoutées il faut ici aussi les rajoutées (enfait nan c bon)
        doneObjs = []
        for category in self.objs:
            for key in self.objs[category]:
                obj = self.objs[category][key]
                if obj not in doneObjs:
                    obj.display()
                    doneObjs.append(obj)
        print("display Stage")

    def create_chunks(self, h1, h2):
        print("*creating chunks*")
        for i in range(16):
            for j in range(9):
                ch = Chunk((i/16)*get_winW(), (j/9)*get_winH(), ((i+1)/16)*get_winW()-1, ((j+1)/9)*get_winH()-1, h1, h2)
                self.chunks[i].append(ch)
                ch.synchronize()



class Floor(Stage):                 # class qui définie le sol
    def __init__(self, y):
        super().__init__()
        self.y = y * get_ratio()+ window.root.oY

    def display(self):              # Création de la "forme" du sol (en gros la partie graphique)
        self.shape = get_can().create_rectangle(0, self.y, window.root.screenW, window.root.screenH, width=0, fill=self.color)


class Ceiling(Stage):               # class qui définie le palfond du niveau
    def __init__(self, y):
        super().__init__()
        self.y = y * get_ratio()+ window.root.oY

    def display(self):
        self.shape = get_can().create_rectangle(0, 0, window.root.screenW, self.y, width=0, fill=self.color)


class WallLeft(Stage):                # class qui definie le mur de gauche 
    def __init__(self, x):
        super().__init__()
        self.x = x * get_ratio() + window.root.oX

    def display(self):
        self.shape = get_can().create_rectangle(0, 0, self.x, window.root.screenH, width=0, fill=self.color)


class WallRight(Stage):                 # class qui definie le mur de droite 
    def __init__(self, x):
        super().__init__()
        self.x = x * get_ratio() + window.root.oX

    def display(self):
        self.shape = get_can().create_rectangle(self.x, 0, window.root.screenW, window.root.screenH, width=0, fill=self.color)


class Block(Stage):
    def __init__(self, state, x, y, sX, sY, num):
        super().__init__()
        self.x, self.y = x * get_ratio() + window.root.oX, y * get_ratio() + window.root.oY
        self.sizeX, self.sizeY = sX * get_ratio(), sY * get_ratio()
        self.state = state
        self.num = num

    
    def display(self):
        self.shape = get_can().create_rectangle(self.x, self.y, 
                self.x + self.sizeX, self.y + self.sizeY, width=0, fill=self.color)


class Platform(Block):
    def __init__(self, state, x, y, sX, sY, dx, dy, num):
        self.block = Block(state, x, y, sX, sY, num)
        self.dx, self.dy = dx * get_ratio(), dy * get_ratio()

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

    
class Chunk():
    def __init__(self, x1, y1, x2, y2, h1, h2):
        self.objs = []
        self.x1, self.y1, self.x2, self.y2 = x1*get_ratio() + window.root.oX, y1*get_ratio() + window.root.oY, x2*get_ratio() + window.root.oX, y2*get_ratio() + window.root.oY
        self.hero1, self.hero2 = h1, h2
        self.state = [None, None]

    def activate(self, heroNum):
        if self.objs:
            self.state[heroNum] = True

    def desactivate(self, heroNum):
        self.state[heroNum] = False
    
    def calculate(self):
        # if ((self.x1 < self.hero.x < self.x2) or (self.x1 < self.hero.x + self.hero.size < self.x2)) and ((self.y1 < self.hero.y < self.y2) or (self.y1 < self.hero.y + self.hero.size < self.y2)):
        if ((self.x1 <= self.hero1.x <= 2*self.x2 - self.x1) or (2*self.x1 - self.x2 <= self.hero1.x + self.hero1.size <= self.x2)) and (
            (self.y1 <= self.hero1.y <= 2*self.y2 - self.y1) or (2*self.y1 - self.y2 <= self.hero1.y + self.hero1.size <= self.y2)):
            self.activate(0)
        else:
            self.desactivate(0)

        if ((self.x1 <= self.hero2.x <= 2*self.x2 - self.x1) or (2*self.x1 - self.x2 <= self.hero2.x + self.hero2.size <= self.x2)) and (
            (self.y1 <= self.hero2.y <= 2*self.y2 - self.y1) or (2*self.y1 - self.y2 <= self.hero2.y + self.hero2.size <= self.y2)):
            self.activate(1)
        else:
            self.desactivate(1)

    def synchronize(self):              # Met les objets (statiques) présents dans le chunk, dans sa liste objs
        for key in stage0.objs["Block"]:
            obj = stage0.objs["Block"][key]
            if ((self.x1 <= obj.x <= self.x2) or (obj.x <= self.x1 <= self.x2 <= obj.x + obj.sizeX) or (self.x1 <= obj.x + obj.sizeX <= self.x2)) and (
                (self.y1 <= obj.y <= self.y2) or (obj.y <= self.y1 <= self.y2 <= obj.y + obj.sizeY) or (self.y1 <= obj.y + obj.sizeY <= self.y2)):
                self.objs.append(obj)

        

# class Spawn(Stage):                       # En cours de construction..
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y


def get_can():
    return window.root.canvas

def get_ratio():
    return window.root.ratio

def get_winH():
    return window.root.winH

def get_winW():
    return window.root.winW

def create(level, hero1, hero2):              # Crée le niveau demandé
    global stage0               
    objs = []                   # obs correspond aux éléments du niveau, ils seront ajoutés plus tard
    stage0 = Stage(objs)
    commonObjs = {"floor": None, "ceiling": None, "wallLeft": None, "wallRight": None}      # commonObjs c'est les éléments d'un niveau toujours présents (plus tard il y aura des éléments facultatif).
    otherObjs = {"solid": {}, "semi-solid": {}, "block": {}, "platform": {}}
    # A la place des None ils y aura des objets de la classe correspondante.

    file = open(getcwd() + "\\levels\\lvl" + str(level) + ".lvl", "r")      # Ouvre un fichier dans le dossier "levels", ex: "lvl2.lvl"

    count = {"pla": 0, "blo": 0}

    for line in file:           # Prend chaque ligne une par une dans le fichier
        line = line.split()     # line devient une liste de "mots", le 1er est le type d'objet, la suite est ses futurs attributs.

        if line[0] == "floor":                  # On regarde quel est le premier mot, et en fonction de ce
            commonObjs["floor"] = Floor(int(line[1]))
        if line[0] == "ceiling":
            commonObjs["ceiling"] = Ceiling(int(line[1]))
        if line[0] == "wallLeft":
            commonObjs["wallLeft"] = WallLeft(int(line[1]))
        if line[0] == "wallRight":
            commonObjs["wallRight"] = WallRight(int(line[1]))
        
        if line[0] == "block":
            if line[1] == "solid":
                otherObjs["solid"]["block" + str(count["blo"])] = Block(line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), count["blo"])
                otherObjs["block"]["block" + str(count["blo"])] = otherObjs["solid"]["block" + str(count["blo"])]
            elif line[1] == "semi-solid":
                otherObjs["semi-solid"]["block" + str(count["blo"])] = Block(line[1], int(line[2]), int(line[3]),int(line[4]), int(line[5]), count["blo"])
                otherObjs["block"]["block" + str(count["blo"])] = otherObjs["semi-solid"]["block" + str(count["blo"])]
            count["blo"] += 1
        
        if line[0] == "platform":
            if line[1] == "solid":
                otherObjs["solid"]["platform" + str(count["pla"])] = Platform(line[1], int(line[2]), int(line[3]), int(line[4]), 
                                                                                    int(line[5]), float(line[6]), float(line[7]), count["pla"])
                otherObjs["platform"]["platform" + str(count["pla"])] = otherObjs["solid"]["platform" + str(count["pla"])]
            elif line[1] == "semi-solid":
                # otherObjs["semi-solid"].append( Platform(line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7])) )
                otherObjs["semi-solid"]["platform" + str(count["pla"])] = Platform(line[1], int(line[2]), int(line[3]),int(line[4]), 
                                                                                    int(line[5]), float(line[6]), float(line[7]), count["pla"])
                otherObjs["platform"]["platform" + str(count["pla"])] = otherObjs["semi-solid"]["platform" + str(count["pla"])]
            count["pla"] += 1

        # Il faudra rajouter ici d'autres éléments

    stage0 = Stage(commonObjs, otherObjs)
    file.close()                # Enlève le fichier de la mémoire
    for h in hero1, hero2:
        h.onBlock = [False] * count["blo"]
    stage0.create_chunks(hero1, hero2)
