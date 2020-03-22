from tkinter import*
import time


class Stage:
    def __init__(self, list):
        self.objs = list

    def display(self):
        for obj in self.objs:
            obj.display()
        print("display Stage")


class Floor(Stage):
    def __init__(self, y):
        self.y = y

    def display(self):
        self.floor = canvas.create_rectangle(0, self.y, winW, winH, width=0, fill="#D0DCE0")


class Ceiling(Stage):
    def __init__(self, y):
        self.y = y

    def display(self):
        self.ceiling = canvas.create_rectangle(0, 0, winW, self.y, width=0, fill="#D0DCE0")


class WallLeft(Stage):
    def __init__(self, x):
        self.x = x

    def display(self):
        self.wallL = canvas.create_rectangle(0, 0, self.x, winH, width=0, fill="#D0DCE0")


class WallRight(Stage):
    def __init__(self, x):
        self.x = x

    def display(self):
        self.wallR = canvas.create_rectangle(self.x, 0, winW, winH, width=0, fill="#D0DCE0")


class Hero:         # C'est la classe des carrés
    def __init__(self, x, y, c, co):      # __init__ est exécuté à la création d'un objet (carré), "self" est obligatoire laisse tomber
        self.x = x                       # x, y, s et c sont les attributs indiqués à la création des carrés (ligne 36)
        self.y = y                       # ensuite on défini les variables du carré grâce aux attributs
        self.size = 50
        self.color = c
        self.hero = canvas.create_rectangle(self.x, self.y,                                 # Création du carré graphiquement
                                            self.x + self.size, self.y + self.size,         # L'origine du carré est sur le sommet en haut à droite
                                            fill = self.color, width = 0)
        self.ax, self.ay = 0, 0.075
        self.vx, self.vy = 0, 0
        self.controls = {"droite": co[0], "gauche": co[1], "saut": co[2]}
        self.onFloor = True
        self.heroCollisionY = 3         # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "y supérieur à l'autre", 3 = autres conditions


    def p_droite(self, event):
        keys[self.controls["droite"]] = True
        self.set_vx()

    def p_gauche(self, event):
        keys[self.controls["gauche"]] = True
        self.set_vx()

    def r_droite(self, event):
        keys[self.controls["droite"]] = False
        self.set_vx()

    def r_gauche(self, event):
        keys[self.controls["gauche"]] = False
        self.set_vx()

    def p_saut(self, event):
        if keys[self.controls["saut"]] == False and (self.onFloor == True or self.heroCollisionY == 1): # Pour sauter une seule fois jusqu'à toucher le sol
            keys[self.controls["saut"]] = True
            self.vy = -3
            self.onFloor = False
            if self.heroCollisionY == 1:
                self.heroCollisionY = 2
            # print("hop")

    def r_saut(self, event):
        keys[self.controls["saut"]] = False



    def set_vx(self):           # Si les touches "droite" et "gauche" sont pressées, le héro ne doit pas bouger
        if keys[self.controls["droite"]] == True:
            vxSum = 1
        else:
            vxSum = 0
        if keys[self.controls["gauche"]] == True:
            vxSum -= 1
        self.vx = vxSum
        # print(self.vx)

    def set_vy(self):
        if self.onFloor == False and self.heroCollisionY != 1:
            self.vy += self.ay          # On augmente la vitesse vers le bas grâce à l'accélération (gravité)


    def collide_hero(self, otherX, otherY, otherOnFloor):
    
        if self.heroCollisionY == 1:        # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "'y' supérieur à l'autre", 3 = autres conditions
            if self.x > otherX - self.size and self.x < otherX + self.size:     # Si le hero est dans l'intervalle de collision (x) : False ou True
                self.y = otherY - self.size
                self.vy = 0
            else:
                self.heroCollisionY = 3
                # print("#3")

        elif otherOnFloor:            
            if self.vy >= 0:            # Modification :  > → >=
                if self.y + self.size < otherY:
                    self.heroCollisionY = 2         
                    # print("#2")
                elif self.heroCollisionY == 2:      # Est-ce que juste avant le carré qui tombe était au dessus de l'autre ??
                    ratio = (self.y - canvas.coords(self.hero)[1]) / (otherY - self.size - canvas.coords(self.hero)[1])         # Modification (- self.size)
                    heroCollisionX = (self.x - canvas.coords(self.hero)[0]) / ratio + canvas.coords(self.hero)[0]

                    if heroCollisionX > otherX - self.size and heroCollisionX < otherX + self.size:
                        self.heroCollisionY = 1
                        # print("#1")
                    else:               # Modification : TAB
                        self.heroCollisionY = 3
                        # print("#3")
    
                if self.heroCollisionY == 1:
                    self.y = otherY - self.size
                    self.vy = 0


    def move(self):
        self.set_vy()
        self.x += self.vx * 2
        self.y += self.vy * 2

        if self.y <= ceiling1.y:
            self.y = ceiling1.y + (ceiling1.y - self.y) / 2
            self.vy *= -0.5

        if self.y + self.size > floor1.y:
            if self.onFloor == False:
                self.onFloor = True
                # print("boom")
            self.y = floor1.y - self.size

        if self.x <= wall1.x:
            self.x = wall1.x
            self.vx = 0

        if self.x + self.size >= wall2.x:
            self.x = wall2.x - self.size
            self.vx = 0

        if self.onFloor == False:
            if self.color == hero1.color:         # On teste si le hero est le hero1
                self.collide_hero(hero2.x, hero2.y, hero2.onFloor)
            else:
                self.collide_hero(hero1.x, hero1.y, hero1.onFloor)
        
        coords3 = redCoords()
        canvas.coords(hero3, coords3[0], coords3[1], coords3[2], coords3[3])

        canvas.coords(self.hero, self.x, self.y,
                                 self.x + self.size, self.y + self.size)
        # canvas.move(self.hero, self.vx*2, self.vy*2)
        canvas.update()         # Mise à jour de l'affichage
        canvas.after(10, self.move)     # Recall de la fonction 10ms plus tard



def redCoords():
    if (hero1.y > hero2.y - hero2.size and hero1.y < hero2.y + hero2.size) and (hero1.x > hero2.x - hero2.size and hero1.x < hero2.x + hero2.size):
        x3 = [hero1.x, hero2.x + hero2.size] if hero1.x > hero2.x else [hero2.x, hero1.x + hero1.size]
        y3 = [hero1.y, hero2.y + hero2.size] if hero1.y > hero2.y else [hero2.y, hero1.y + hero1.size]
        return (x3[0], y3[0], x3[1], y3[1])
    else:
        return (-1, -1, -1, -1)


def debug_enter(event):             # /!\ Il ne faut pas écrire n'importe quoi par mesure de sécurité, par exemple : func effacer_tout_les_fichiers()
    command = input("Command > ")
    words = command.split()
    
    if words:
        if words[0] == "help":
            print("-----------------------------------------------")
            print("* func <function>\n    Pour appeller une fonction\n* var <name> <value> <int|float|str> [object]\n    Pour changer la valeur d'une variable")
            print("-----------------------------------------------")

        if words[0] == "func":          # func <function>
            eval(words[1])
            print("The function", words[1], "has been executed")
        
        elif words[0] == "var":         # var <name> <value> <int|float|str> [object]
            if len(words) == 5:
                if words[3] == "int":
                    setattr(eval(words[4]), words[1], int(words[2]))
                elif words[3] == "float":
                    setattr(eval(words[4]), words[1], float(words[2]))
                elif words[3] == "str":
                    setattr(eval(words[4]), words[1], words[2])
                print(words[4] + '.' + words[1], "is now equal to", words[2])

            elif len(words) == 4:
                if words[3] == "int":
                    globals()[words[1]] = int(words[2])
                elif words[3] == "float":
                    globals()[words[1]] = float(words[2])
                elif words[3] == "str":
                    globals()[words[1]] = words[2]
                print(words[1], "is now equal to", words[2])


# Variables de la fenêtre "window"
winH = 540
winW = 960
bg = "white"

# Création de la fenêtre et du canvas(pour faire des "dessins" de carrés et autres)
window = Tk()
canvas = Canvas(height=winH, width=winW, background=bg)

# Affichage du canvas
canvas.pack()


# Dictionnaire de l'état des touches
keys = {'d': False, 'q': False, 'z': False, "Left": False, "Right": False, "Up": False}

floor1 = Floor(450)
ceiling1 = Ceiling(100)
wall1 = WallLeft(50)
wall2 = WallRight(910)
stage1 = Stage([floor1, ceiling1, wall1, wall2])

hero1 = Hero(500, 400, "#de3193", ["Right", "Left", "Up"]) # Création du carré bleu/violet "#007FD3"
hero2 = Hero(200, 400, "#ff8a29", ["d", "q", "z"]) # Création du carré orange "#E69A00"
# Les 2 carrés sont des objets indépendants de type (class) : Hero, donc ils ont les memes attributs (variables)
# et les mêmes fonctions tout en marchant indépendament (en bougeant les coordonées de l'un, l'autre ne bouge pas)

hero3 = canvas.create_rectangle(-1, -1, -1, -1, fill="#ff2e2e", width=0)        # rouge/vert:"#55ff5f"


# Détection des touches
canvas.bind_all('<Right>', hero1.p_droite)
canvas.bind_all('<KeyRelease-Right>', hero1.r_droite)
canvas.bind_all('<Left>', hero1.p_gauche)
canvas.bind_all('<KeyRelease-Left>', hero1.r_gauche)
canvas.bind_all('<Up>', hero1.p_saut)
canvas.bind_all('<KeyRelease-Up>', hero1.r_saut)

canvas.bind_all('<d>', hero2.p_droite)
canvas.bind_all('<KeyRelease-d>', hero2.r_droite)
canvas.bind_all('<q>', hero2.p_gauche)
canvas.bind_all('<KeyRelease-q>', hero2.r_gauche)
canvas.bind_all('<z>', hero2.p_saut)
canvas.bind_all('<KeyRelease-z>', hero2.r_saut)

canvas.bind_all('<Return>', debug_enter)


stage1.display()
# floor1.display()
# ceiling1.display()
# wall1.display()
# wall2.display()

hero1.move()
hero2.move()


window.mainloop()
