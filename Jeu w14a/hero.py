import window               # On importe les sous fichiers dont on aura besoin
import controls
import stage
import graphics


class Hero:         # C'est la classe des carrés
    def __init__(self, x, y, c, co):      # __init__ est exécuté à la création d'un objet (carré), "self" est obligatoire laisse tomber
        self.x = x                       # x, y, s et c sont les attributs indiqués à la création des carrés (ligne 36)
        self.y = y                       # ensuite on défini les variables du carré grâce aux attributs
        self.size = 50
        self.color = c
        self.hero = get_can().create_rectangle(self.x, self.y,                                 # Création du carré graphiquement
                                            self.x + self.size, self.y + self.size,         # L'origine du carré est sur le sommet en haut à droite
                                            fill = self.color, width = 0)
        self.ax, self.ay = 0, 0.075
        self.vx, self.vy = 0, 0
        self.controls = {"droite": co[0], "gauche": co[1], "saut": co[2]}
        self.onFloor = True
        self.heroCollisionY = 3         # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "y supérieur à l'autre", 3 = autres conditions
        controls.init()


    def p_droite(self, event):
        get_keys()[self.controls["droite"]] = True
        self.set_vx()

    def p_gauche(self, event):
        get_keys()[self.controls["gauche"]] = True
        self.set_vx()

    def r_droite(self, event):
        get_keys()[self.controls["droite"]] = False
        self.set_vx()

    def r_gauche(self, event):
        get_keys()[self.controls["gauche"]] = False
        self.set_vx()

    def p_saut(self, event):
        if get_keys()[self.controls["saut"]] == False and (self.onFloor == True or self.heroCollisionY == 1): # Pour sauter une seule fois jusqu'à toucher le sol
            get_keys()[self.controls["saut"]] = True
            self.vy = -3
            self.onFloor = False
            if self.heroCollisionY == 1:
                self.heroCollisionY = 2
            # print("hop")

    def r_saut(self, event):
        get_keys()[self.controls["saut"]] = False



    def set_vx(self):           # Si les touches "droite" et "gauche" sont pressées, le héro ne doit pas bouger
        if get_keys()[self.controls["droite"]] == True:
            vxSum = 1
        else:
            vxSum = 0
        if get_keys()[self.controls["gauche"]] == True:
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
                    ratio = (self.y - get_can().coords(self.hero)[1]) / (otherY - self.size - get_can().coords(self.hero)[1])         # Modification (- self.size)
                    heroCollisionX = (self.x - get_can().coords(self.hero)[0]) / ratio + get_can().coords(self.hero)[0]

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


        if self.y <= get_comObjs("ceiling").y:
            self.y = get_comObjs("ceiling").y + (get_comObjs("ceiling").y - self.y) / 2
            self.vy *= -0.5

        if self.y + self.size > get_comObjs("floor").y:
            if self.onFloor == False:
                self.onFloor = True
                # print("boom")
            self.y = get_comObjs("floor").y - self.size

        if self.x <= get_comObjs("wallLeft").x:
            self.x = get_comObjs("wallLeft").x
            self.vx = 0

        if self.x + self.size >= get_comObjs("wallRight").x:
            self.x = get_comObjs("wallRight").x - self.size
            self.vx = 0

        if self.onFloor == False:
            if self.color == hero1.color:         # On teste si le hero est le hero1
                self.collide_hero(hero2.x, hero2.y, hero2.onFloor)
            else:
                self.collide_hero(hero1.x, hero1.y, hero1.onFloor)
        
        coords3 = graphics.redCoords(hero1, hero2)
        get_can().coords(graphics.hTransparency, coords3[0], coords3[1], coords3[2], coords3[3])

        get_can().coords(self.hero, self.x, self.y,
                                 self.x + self.size, self.y + self.size)
        # get_can().move(self.hero, self.vx*2, self.vy*2)
        get_can().update()         # Mise à jour de l'affichage
        get_can().after(10, self.move)     # Recall de la fonction 10ms plus tard



def init(co1, co2):
    global hero1, hero2
    hero1 = Hero(co1[0], co1[1], "#de3193", ["Right", "Left", "Up"]) # Création du carré bleu/violet "#007FD3"
    hero2 = Hero(co2[0], co2[1], "#ff8a29", ["d", "q", "z"]) # Création du carré orange "#E69A00"
    # Les 2 carrés sont des objets indépendants de type (class) : Hero, donc ils ont les memes attributs (variables)
    # et les mêmes fonctions tout en marchant indépendament (en bougeant les coordonées de l'un, l'autre ne bouge pas)

def get_can():
    return window.root.canvas

def get_keys():
    return controls.keys

def get_comObjs(name):
    return stage.stage0.objs["Common"][name]
