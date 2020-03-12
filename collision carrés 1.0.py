from tkinter import*
import time


class Stage:
    '''def __init__(self):'''
    def display(self):
        print("display Stage")



class Floor(Stage):
    def __init__(self, y):
        self.y = y

    def display(self):
        canvas.create_rectangle(0, self.y, winW, winH, width=0, fill="#D0DCE0")



class Hero:         # C'est la classe des carrés
    def __init__(self, x, y, c, co):      # __init__ est exécuté à la création d'un objet (carré), "self" est obligatoire laisse tomber
        self.x = x                       # x, y, s et c sont les attributs indiqués à la création des carrés (ligne 36)
        self.y = y                       # ensuite on défini les variables du carré grâce aux attributs
        self.size = 50
        self.color = c
        self.hero = canvas.create_rectangle(self.x, self.y,                                 # Création du carré graphiquement
                                            self.x + self.size, self.y + self.size,         # L'origine du carré est sur le sommet en haut à droite
                                            fill = self.color, width = 0)
        self.ax, self.ay = 0, 0.08
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
            print("hop")

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
        print(self.vx)

    def set_vy(self):
        if self.onFloor == False and self.heroCollisionY != 1:
            self.vy += self.ay          # On augmente la vitesse vers le bas grâce à l'accélération (gravité)

    def collide_hero(self, otherX, otherY, otherOnFloor):

        heroesSameX = (self.x > otherX - self.size and self.x < otherX + self.size)    # Si le hero est dans l'intervalle de collision (x) : False ou True

        if self.heroCollisionY == 1:
            if heroesSameX:
                self.y = otherY - self.size
                self.vy = 0
            else:
                self.heroCollisionY = 3
                print("#3")

        elif otherOnFloor == True:            
            if self.vy > 0:
                if self.y + self.size < otherY:
                    self.heroCollisionY = 2         # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "'y' supérieur à l'autre", 3 = autres conditions
                    print("#2")
                elif self.heroCollisionY == 2:      # Est-ce que juste avant le carré qui tombe était au dessus de l'autre ??
                    ratio = (self.y - canvas.coords(self.hero)[1]) / (otherY - canvas.coords(self.hero)[1])
                    heroCollisionX = (self.x - canvas.coords(self.hero)[0]) / ratio + canvas.coords(self.hero)[0]

#--------------------------------------------- DEBUG ----------------------------------------------------
                    canvas.coords(debugSpot, heroCollisionX, otherY, heroCollisionX+2, otherY+2)
                    canvas.update()
                    time.sleep(1)
                    canvas.coords(debugSpot, -1, -1, -1, -1)
                    canvas.update()
#--------------------------------------------------------------------------------------------------------

                    if heroCollisionX > otherX - self.size and heroCollisionX < otherX + self.size:
                        self.heroCollisionY = 1
                        print("#1")
                else:
                    self.heroCollisionY = 3
                    print("#3")
                
                if self.heroCollisionY == 1:
                    self.y = otherY - self.size
                    self.vy = 0


    def move(self):
        self.set_vy()
        self.x += self.vx * 2
        self.y += self.vy * 2

        if self.y + self.size > floor1.y:
            if self.onFloor == False:
                self.onFloor = True
                print("boom")
            # try:
            #     ratio = (self.y+self.size - canvas.coords(self.hero)[3]) / (floor1.y - canvas.coords(self.hero)[3])
            #     self.x = (self.x-self.size - canvas.coords(self.hero)[0]) / ratio + canvas.coords(self.hero)[0]
            # except:
            #     print("error")
            self.y = floor1.y - self.size

        if self.onFloor == False:
            if self.color == "#007FD3":         # On teste si le hero est bleu, soit le hero1
                self.collide_hero(hero2.x, hero2.y, hero2.onFloor)
            else:
                self.collide_hero(hero1.x, hero1.y, hero1.onFloor)

        canvas.coords(self.hero, self.x, self.y,
                                 self.x + self.size, self.y + self.size)
        # canvas.move(self.hero, self.vx*2, self.vy*2)
        canvas.update()         # Mise à jour de l'affichage
        canvas.after(10, self.move)     # Recall de la fonction 10ms plus tard








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

hero1 = Hero(500, 400, "#007FD3", ["Right", "Left", "Up"]) # Création du carré bleu
hero2 = Hero(200, 400, "#E69A00", ["d", "q", "z"]) # Création du carré orange
# Les 2 carrés sont des objets indépendants de type (class) : Hero, donc ils ont les memes attributs (variables)
# et les mêmes fonctions tout en marchant indépendament (en bougeant les coordonées de l'un, l'autre ne bouge pas)

debugSpot = canvas.create_line(-1, -1, -1, -1, fill="red", width=2)


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


floor1.display()
hero1.move()
hero2.move()


window.mainloop()
