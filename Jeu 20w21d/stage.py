''' Voici le module qui définie les éléments d'un niveau '''

import window                           
from os import getcwd               # Pour obtenir le chemin d'accès du fichier actuel dans l'arborescence.
import debug
import graphics
import time
from threading import Thread


class Stage:
    def __init__(self, lvl=False):
        if lvl:             # Pour ne pas changer ce dictionnaire quand une sous classe est créée (elle ne spécierais pas lvl)
            self.objs = {}          # Initiation, le dictionnaire sera bientôt rempli
            self.chunks = []
            self.level = lvl
        self.color = ("#AAB3B3", "#D0DCE0")
        self.height, self.width = window.root.winH, window.root.winW
        print(">>>>", self.height, self.width)

    def display(self):              # /!\ Si des listes d'éléments sont rajoutées il faut ici aussi les rajoutées (enfait nan c bon)
        doneObjs = []
        for category in self.objs:
            if category in ("Spawn", "Win"):
                continue
            for key in self.objs[category]:
                obj = self.objs[category][key]
                if obj not in doneObjs:
                    obj.display()
                    doneObjs.append(obj)
        print("display Stage")

    def create_chunks(self):
        print("*creating chunks*")
        numCol = int(self.width / 60)       # Nb de colonnes, donc nb de chunks par ligne (un chunk est de taille 60)
        numRow = int(self.height / 60)      
        print("nb chunk", numCol, numRow)
        for i in range(numCol):
            col = []
            for j in range(numRow):
                ch = Chunk((i/numCol) * self.width, (j/numRow) * self.height, 
                    (i/numCol) * self.width + 60, (j/numRow) * self.height + 60, hero1, hero2)
                col.append(ch)
                ch.synchronize()            # Le chunk est synchronisé avec tous les objets autour de lui
            self.chunks.append(col)      # On rajoute toutes la colonnes de chunks à la matrice chunks


class Floor(Stage):                 # class qui définie le sol
    def __init__(self, y):
        super().__init__()
        self.y = y

    def display(self):              # Création de la "forme" du sol (en gros la partie graphique)
        self.shape = get_can().create_rectangle(0, self.y*get_ratio()+get_oY(), window.root.screenW, window.root.screenH, width=0, fill=self.color[0])


class Ceiling(Stage):               # class qui définie le palfond du niveau
    def __init__(self, y):
        super().__init__()
        self.y = y

    def display(self):
        self.shape = get_can().create_rectangle(0, 0, window.root.screenW, self.y*get_ratio()+get_oY(), width=0, fill=self.color[0])


class WallLeft(Stage):                # class qui definie le mur de gauche 
    def __init__(self, x):
        super().__init__()
        self.x = x

    def display(self):
        self.shape = get_can().create_rectangle(0, 0, self.x*get_ratio()+get_oX(), window.root.screenH, width=0, fill=self.color[0])


class WallRight(Stage):                 # class qui definie le mur de droite 
    def __init__(self, x):
        super().__init__()
        self.x = x

    def display(self):
        self.shape = get_can().create_rectangle(self.x*get_ratio()+get_oX(), 0, window.root.screenW, window.root.screenH, width=0, fill=self.color[0])


class Block(Stage):
    def __init__(self, state, x, y, sX, sY, num):
        super().__init__()
        self.x, self.y = x, y
        # print("YYYYYYYYY", self.y)
        self.sizeX, self.sizeY = sX, sY
        self.state = state
        self.color = self.color[0] if self.state == "solid" else self.color[1]
        self.num = num

    
    def display(self):
        self.shape = get_can().create_rectangle(self.x*get_ratio()+get_oX(), self.y*get_ratio()+get_oY(), 
                self.x*get_ratio()+get_oX() + self.sizeX*get_ratio(), self.y*get_ratio()+get_oY() + self.sizeY*get_ratio(),
                 width=0, fill=self.color)


class Platform():
    def __init__(self, state, x, y, sX, sY, dx, dy, num):
        self.block = Block(state, x, y, sX, sY, num)
        self.dx, self.dy = dx, dy

    def move(self):
        self.move_update()
        get_can().move(self.block.shape, self.dx*get_ratio(), self.dy*get_ratio())
        # get_can().coords(self.block.shape, self.block.x*get_ratio()+get_oX(), self.block.y*get_ratio()+get_oY(),
        #             self.block.x*get_ratio()+get_oX() + self.block.sizeX*get_ratio(),
        #             self.block.y*get_ratio()+get_oY() + self.block.sizeY*get_ratio())

    def move_update(self):
        x1, y1, x2, y2 = self.block.x, self.block.y, self.block.x + self.block.sizeX, self.block.y + self.block.sizeY

        if x1 < 0 or x2 > self.block.width:     # block.width correspond à la largeur du niveau
            self.dx *= -1
        if y1 < 0 or y2 > self.block.height:
            self.dy *= -1
        
        self.block.x += self.dx
        self.block.y += self.dy
        

    def display(self):
        self.block.display()

    
class Chunk():
    def __init__(self, x1, y1, x2, y2, h1, h2):
        self.objs = []
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.hero1, self.hero2 = h1, h2
        self.state = [None, None]
        # print("___", x1, y1, x2, y2)
        # print("~~~", self.x1, self.y1, self.x2, self.y2)

    def activate(self, heroNum):
        if self.objs:
            self.state[heroNum] = True

    def desactivate(self, heroNum):
        self.state[heroNum] = False
    
    def calculate(self):
        # if ((self.x1 < self.hero.x < self.x2) or (self.x1 < self.hero.x + self.hero.size < self.x2)) and ((self.y1 < self.hero.y < self.y2) or (self.y1 < self.hero.y + self.hero.size < self.y2)):
        if (
            (self.x1 <= self.hero1.x <= 2*self.x2 - self.x1) or 
            (2*self.x1 - self.x2 <= self.hero1.x + self.hero1.size <= self.x2)) and (
            (self.y1 <= self.hero1.y <= 2*self.y2 - self.y1) or 
            (2*self.y1 - self.y2 <= self.hero1.y + self.hero1.size <= self.y2)
        ):
            self.activate(0)
        else:
            self.desactivate(0)

        if (
            (self.x1 <= self.hero2.x <= 2*self.x2 - self.x1) or 
            (2*self.x1 - self.x2 <= self.hero2.x + self.hero2.size <= self.x2)) and (
            (self.y1 <= self.hero2.y <= 2*self.y2 - self.y1) or 
            (2*self.y1 - self.y2 <= self.hero2.y + self.hero2.size <= self.y2)
        ):
            self.activate(1)
        else:
            self.desactivate(1)

    def synchronize(self):              # Met les objets (statiques) présents dans le chunk, dans sa liste objs
        for key in stage0.objs["Block"]:
            obj = stage0.objs["Block"][key]
            if ((self.x1 <= obj.x <= self.x2) or (obj.x <= self.x1 <= self.x2 <= obj.x + obj.sizeX) or (self.x1 <= obj.x + obj.sizeX <= self.x2)) and (
                (self.y1 <= obj.y <= self.y2) or (obj.y <= self.y1 <= self.y2 <= obj.y + obj.sizeY) or (self.y1 <= obj.y + obj.sizeY <= self.y2)):
                self.objs.append(obj)

    
class Spawn(Stage):
    def __init__(self, hero, x, y):
        self.x = x
        self.y = y
        self.hero = hero
        self.tp_spawn()
        
    def tp_spawn(self):
        self.hero.x = self.x
        self.hero.y = self.y


class Win():
    def __init__(self, heroes, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.heroes = heroes

        if len(heroes) == 2:
            self.color = "red"
        elif heroes[0].color == "#ff8a29":
            self.color = "orange"
        else:
            self.color = "purple"

        self.shape1 = get_can().create_rectangle(self.x1*get_ratio()+get_oX(), self.y1*get_ratio()+get_oY(),
                                            self.x2*get_ratio()+get_oX() , self.y2*get_ratio()+get_oY())
        self.flag = graphics.Texture("textures\\flags\\"+self.color+"_flag.png", 50, 50, (x1+x2)/2, y2-25)

    def test(self):         # Teste si les conditions de victoire sont validées
        count = 0
        for h in self.heroes:
            if self.x2 >= h.x and self.x1 <= h.x + h.size and self.y2 >= h.y and self.y1 <= h.y + h.size:
                count += 1
        if count == len(self.heroes):       # Si tous les héros sont dans la zone 
            return True


def stage_end():
    global hasWon
    if not hasWon:
        hasWon = True
        print("wp")
        return time.time()

# def victory_time():
#     debug.debugger.stop = True
#     print("____________________________________")
#     change_level(stage0.level+1)

def change_level(lvl):
    debug.debugger.stop = True
    time.sleep(0.5)             # Sécurité
    get_can().delete("all")
    create(lvl)
    stage0.display()

    for h in hero1, hero2:            # Affiche les carrés devant tout le reste
        h.display()
        get_can().tag_raise(h.shape)
        h.ax, h.ay = 0, 0.075
        h.vx, h.vy = 0, 0
        h.onFloor = False
    graphics.init()                                 # Les bonus graphiques
    get_can().tag_raise(window.root.shape)

    for key in stage0.objs["Win"]:
        get_can().tag_raise(stage0.objs["Win"][key].shape1)
        get_can().tag_raise(stage0.objs["Win"][key].flag.shape)

    # print("presque.....")
    # time.sleep(2)
    debug.debugger.stop = False

def create(level):              # Crée le niveau demandé
    global stage0               
    stage0 = Stage(level)
    technicalObjs = {"spawn": [1, 2], "win": {}}
    commonObjs = {"floor": None, "ceiling": None, "wallLeft": None, "wallRight": None}      # commonObjs c'est les éléments d'un niveau toujours présents (plus tard il y aura des éléments facultatif).
    otherObjs = {"solid": {}, "semi-solid": {}, "block": {}, "platform": {}}
    get_can().delete("all")
    # A la place des None ils y aura des objets de la classe correspondante.

    file = open(getcwd() + "\\levels\\lvl" + str(level) + ".lvl", "r")      # Ouvre un fichier dans le dossier "levels", ex: "lvl2.lvl"

    count = {"blo": 0}      # Compte le nombre de block (les plateformes comptent pour des blocs)

    for line in file:           # Prend chaque ligne une par une dans le fichier
        line = line.split()     # line devient une liste de "mots", le 1er est le type d'objet, la suite est ses futurs attributs.
        if not line:
            continue            # Si c'est une ligne vide, on passe à la suivante

        if line[0] == "stage":                  # On regarde quel est le premier mot de chaque ligne, et on fait en fonction
            window.root.calibrate(int(line[1]), int(line[2]))
            stage0.height, stage0.width = window.root.winH, window.root.winW
        
        if line[0] == "spawn":
            heroNum = int(line[1])
            h = hero1 if heroNum == 1 else hero2
            technicalObjs["spawn"][heroNum - 1] = Spawn(h, int(line[2]), int(line[3]))
        if line[0] == "win":
            h = []                  
            if int(line[1]) != 2:       # Si on a un "0", les héros 1 et 2 sont mis dans la liste h.
                h.append(hero1)
            if int(line[1]) != 1:
                h.append(hero2)
            technicalObjs["win"]["win" + line[1]] = Win(h, int(line[2]), int(line[3]), int(line[4]), int(line[5]))

        if line[0] == "floor":                  
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
                otherObjs["solid"]["platform" + str(count["blo"])] = Platform(line[1], int(line[2]), int(line[3]), int(line[4]), 
                                                                                    int(line[5]), float(line[6]), float(line[7]), count["blo"])
                otherObjs["platform"]["platform" + str(count["blo"])] = otherObjs["solid"]["platform" + str(count["blo"])]
            elif line[1] == "semi-solid":
                # otherObjs["semi-solid"].append( Platform(line[1], int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7])) )
                otherObjs["semi-solid"]["platform" + str(count["blo"])] = Platform(line[1], int(line[2]), int(line[3]),int(line[4]), 
                                                                                    int(line[5]), float(line[6]), float(line[7]), count["blo"])
                otherObjs["platform"]["platform" + str(count["blo"])] = otherObjs["semi-solid"]["platform" + str(count["blo"])]
            count["blo"] += 1

        # Il faudra rajouter ici d'autres éléments

    stage0.objs = {"Common": commonObjs, "Spawn": technicalObjs["spawn"], "Win": technicalObjs["win"],
                "Solid": otherObjs["solid"], "Semi_Solid": otherObjs["semi-solid"], 
                "Platform": otherObjs["platform"], "Block": otherObjs["block"]}          # Des plateformes peuvent être à la fois dans Platform et (Semi_)Solid   
    print(stage0.objs)
    file.close()                # Enlève le fichier de la mémoire
    # global win1
    # win1 = Win(100, 200, 200, 300, (hero1, hero2))
    for h in hero1, hero2:          # On met une liste avec pluieurs valeurs Fausses pour chaque blocs
        h.onBlock = [False] * count["blo"]
    stage0.create_chunks()

def init(h1, h2):
    global hero1, hero2, hasWon, winTimeCount
    hero1 = h1
    hero2 = h2
    hasWon = False
    winTimeCount = 0

def get_can():
    return window.root.canvas

def get_ratio():
    return window.root.ratio

def get_oX():
    return window.root.oX

def get_oY():
    return window.root.oY
