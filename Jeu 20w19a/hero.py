''' Voici le module définissant les personnages et ce qui s'y rapportent '''

import window               # On importe les sous fichiers dont on aura besoin
import controls
import stage
import music



class Hero:         # C'est la classe des carrés
    def __init__(self, num, x, y, c, co):      # __init__ est exécuté à la création d'un objet (carré), "self" est obligatoire laisse tomber
        self.num = num
        self.x = x * get_ratio() + window.root.oX         # x, y, s et c sont les attributs indiqués à la création des carrés (ligne 36)
        self.y = y * get_ratio() + window.root.oY         # ensuite on défini les variables du carré grâce aux attributs
        self.size = 50 * get_ratio()
        self.color = c
        self.shape = get_can().create_rectangle(self.x, self.y,                                 # Création du carré graphiquement
                                            self.x + self.size, self.y + self.size,         # L'origine du carré est sur le sommet en haut à droite
                                            fill = self.color, width = 0)
        self.ax, self.ay = 0, 0.075        # Accélération (les physiques ne fonctionnent pas avec des forces mais juste des accélérations)
        self.vx, self.vy = 0, 0                 # Vitesse
        self.controls = {"droite": co[0], "gauche": co[1], "saut": co[2]}       # Touches (inputs)
        self.onFloor = True
        self.onBlock = []
        self.heroCollisionY = 3         # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "y supérieur à l'autre", 3 = autres conditions


    def p_droite(self, event):                  # La touche est pressée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant VRAI
        get_keys()[self.controls["droite"]] = True
        # self.set_vx()

    def p_gauche(self, event):                  # La touche est pressée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant VRAI
        get_keys()[self.controls["gauche"]] = True
        # self.set_vx()

    def r_droite(self, event):                  # La touche est relachée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant FAUX
        get_keys()[self.controls["droite"]] = False
        # self.set_vx()

    def r_gauche(self, event):                  # La touche est relachée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant FAUX
        get_keys()[self.controls["gauche"]] = False
        # self.set_vx()

    def p_saut(self, event):                    # La touche est pressée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant VRAI
        if get_keys()[self.controls["saut"]] == False and (self.onFloor == True or self.heroCollisionY == 1): # Pour sauter une seule fois jusqu'à toucher le sol
            get_keys()[self.controls["saut"]] = True
            # self.vy = -2 if self.heroCollisionY == 0 else -2.9                  # Accélération vers le haut : le saut
            self.vy = -2.9
            self.onFloor = False            # On a décollé du sol
            music.jump()
            if self.heroCollisionY == 1:       
                self.heroCollisionY = 2      # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "'y' supérieur à l'autre", 3 = autres conditions
                self.get_other().heroCollisionY = 3
                self.ay, self.get_other().ay = 0.075, 0.075

    def r_saut(self, event):
        get_keys()[self.controls["saut"]] = False

    def get_other(self):
        return hero2 if self.num == 1 else hero1

    def set_vx(self):           # Si les touches "droite" et "gauche" sont pressées, le héro ne doit pas bouger : 1-1=0
        if get_keys()[self.controls["droite"]] == True:
            vxSum = 1       # Met vitesse à 1 (droite)
        else:
            vxSum = 0       # Met vitesse à 0 (immobile)
        if get_keys()[self.controls["gauche"]] == True:
            vxSum -= 1      # Soustrait vitesse de 1 (gauche)

        if self.onFloor or self.heroCollisionY == 1:    # Pas en l'air
            self.vx = vxSum
        else:                       # En l'air
            self.ax = vxSum
            if self.ax == 0:
                self.vx *= 0.95
            elif (self.ax > 0 and self.vx < 1) or (self.ax < 0 and self.vx > -1):          # Si pas trop rapide..
                self.vx += self.ax / 12
                if self.vx > 1:
                    self.vx = 1
                elif self.vx < -1:
                    self.vx = -1
        if self.vx > 2:                 # Sécurité pour ne pas voyager dans le temps à la vitesse de la lumière
            self.vx = 2         
        elif self.vx < -2:
            self.vx = -2 
        # print(self.ax, self.vx)

    def set_vy(self):
        if not self.onFloor and self.heroCollisionY != 1:          # Si le carré n'est pas sur le sol, ni sur l'autre carré..
            self.vy += self.ay          # On augmente la vitesse vers le bas grâce à l'accélération (gravité)


    def collide_hero(self, other):           # Détection de collision entre les personnages(seul la partie haute des carrés est "solide")
        if self.heroCollisionY == 1:        # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "'y' supérieur à l'autre", 3 = autres conditions
            if self.x > other.x - self.size and self.x < other.x + self.size:     # Si le hero est dans l'intervalle de collision (x): False ou True
                self.y = other.y - other.size                       
                self.vy = other.vy
                other.heroCollisionY = 0
            else:
                self.heroCollisionY = 3
                other.heroCollisionY = 3
                self.ay, other.ay = 0.075, 0.075
                # print("#3")

        # elif other.onFloor:            # Le carré ne se pose sur l'autre seulement si ce dernier est posé au sol
        #     if self.vy >= 0:            # Si au-dessus..
        elif self.vy >= other.vy:
            if self.y + self.size < other.y:     # Si le bas du carré est au-dessus de l'autre..
                self.heroCollisionY = 2         
                # print("#2")
            elif self.heroCollisionY == 2:      # Est-ce que juste avant le carré qui tombe était au dessus de l'autre ??
                try:            # Pour éviter les divisions par 0
                    ratio = (self.y - get_can().coords(self.shape)[1]) / (other.y - get_can().coords(self.shape)[3])        # Thalès pour trouver le point de collision en x
                    heroCollisionX = (self.x - get_can().coords(self.shape)[0]) / ratio + get_can().coords(self.shape)[0]
                except:
                    heroCollisionX = self.x
                if heroCollisionX > other.x - self.size and heroCollisionX < other.x + self.size:
                    self.heroCollisionY = 1             # Il s'est posé sur l'autre carré au moment de la collision
                    # print("#1")
                else:
                    self.heroCollisionY = 3             # Il est passé à côté
                    # print("#3")
            if self.heroCollisionY == 1:            # Comme il s'est posé, on met les bonnes coordonées et la bonne vitesse
                if not other.onFloor and self.vy > 0:
                    other.vy += self.vy*0.3
                self.y = other.y - other.size
                self.ay, other.ay = 0.15, 0.15
                self.vy = other.vy
                other.heroCollisionY = 0
                
        else:
            if self.y + self.size < other.y:     # Si le bas du carré est au-dessus de l'autre..
                self.heroCollisionY = 2
            
    def collide_hero_2(self, other):
        if self.heroCollisionY == 1:
            # if True in self.onBlock:
            if self.onFloor:
                self.heroCollisionY, other.heroCollisionY = 2, 3
                self.ay, other.ay = 0.075, 0.075

    def collide_block(self, block, other):
        if block.state == "solid":
            if self.x + self.size > block.x and self.x < block.x + block.sizeX:
                if self.y + self.size > block.y and self.y < block.y + block.sizeY:
                    if get_can().coords(self.shape)[2] <= block.x:              # hero provient de la gauche ?
                        self.x = block.x - self.size
                        self.ax, self.vx = 0, 0
                    elif get_can().coords(self.shape)[0] >= block.x + block.sizeX:      # hero provient de la droite ?
                        self.x = block.x + block.sizeX
                        self.ax, self.vx = 0, 0
                    elif get_can().coords(self.shape)[3] <= block.y:              # hero provient d'en haut ?
                        self.y = block.y - self.size
                        self.onBlock[block.num], self.onFloor = True, True         # L'avantage d'utiliser onBlock en plus : il ne peut être changé que ici contrairement à onFloor, donc on peut tester si avant le hero était sur le block
                        self.vy = 0
                    elif get_can().coords(self.shape)[1] >= block.y + block.sizeY:      # hero provient d'en bas ?
                        self.y = block.y + block.sizeY + (block.y + block.sizeY - self.y) / 4
                        self.vy *= -0.5
                        if self.heroCollisionY == 1:
                            other.y = block.y + block.sizeY + (block.y + block.sizeY - self.y) / 4 + self.size
                            other.vy *= -0.5
                            self.change(other)
                        # elif (other.y - block.y - block.sizeY >= self.size) and (self.y > other.y - self.size):      
                        #     self.y = other.y - self.size        # Quand il y a juste la place entre l'autre carré et le plafond
                        #     self.vy = 0
                        #     self.heroCollisionY, other.heroCollisionY = 1, 0
                elif self.onBlock[block.num] and self.vy != 0:
                    self.onBlock[block.num], self.onFloor = False, False
            elif self.onBlock[block.num]:
                self.onBlock[block.num], self.onFloor = False, False

        elif block.y <= self.y + self.size and self.vy >= 0:        # "semi-solid"
            if get_can().coords(self.shape)[3] <= block.y:
                try:
                    ratio = (self.y - get_can().coords(self.shape)[1]) / (block.y - get_can().coords(self.shape)[3])        # Thalès pour trouver le point de collision en x
                    collisionX = (self.x - get_can().coords(self.shape)[0]) / ratio + get_can().coords(self.shape)[0]
                except:
                    collisionX = self.x
                if block.x <= collisionX + self.size and collisionX <= block.x + block.sizeX:
                    self.y = block.y - self.size
                    self.onBlock[block.num], self.onFloor = True, True
                    self.vy = 0
            if not (self.x + self.size > block.x and self.x < block.x + block.sizeX) and self.onBlock[block.num]:
                self.onBlock[block.num], self.onFloor = False, False
        elif self.onBlock[block.num] and self.vy != 0:
                    self.onBlock[block.num], self.onFloor = False, False
    
    def change(self, other):
        get_can().coords(other.shape, other.x, other.y,         # Les calculs sont finis, on change les coordonées
                                 other.x + other.size, other.y + other.size)

    def move(self):                 # Méthode pour bouger les personnages
        self.set_vy()
        self.set_vx()
        other = self.get_other()
        if self.heroCollisionY == 1:
            self.vx += other.vx
        self.x += self.vx * 2 * get_ratio()           # Projection des futures coordonées
        self.y += self.vy * 2 * get_ratio()

        # if self.onFloor == False:
        self.collide_hero(other)      # On teste si le hero est le hero1, et en méthode on appelle une méthode avec pas les attributs de l'autre carré
        
        if self.y <= get_comObjs("ceiling").y:          # Détection du Plafond
            self.y = get_comObjs("ceiling").y + (get_comObjs("ceiling").y - self.y) / 4     # La distance au dessus du plafond est mise en dessous (/2), mais est + petite dû à l'élasticité (/2)
            self.vy *= -0.5     # Elasticité
            if self.heroCollisionY == 1:        # Si il est porté, l'autre doit rebondir aussi
                other.y = get_comObjs("ceiling").y + (get_comObjs("ceiling").y - self.y) / 4 + self.size
                other.vy *= -0.5
                self.change(other)
            # elif other.y - get_comObjs("ceiling").y >= self.size and self.y > other.y - self.size:      
            #     self.y = other.y - self.size        # Quand il y a juste la place entre l'autre carré et le plafond
            #     self.vy = 0
            #     self.heroCollisionY, other.heroCollisionY = 1, 0

        if self.y + self.size > get_comObjs("floor").y:         # Détection du sol
            self.onFloor = True
                # print("boom")
            self.y = get_comObjs("floor").y - self.size
            self.vy = 0

        if self.x <= get_comObjs("wallLeft").x:         # Détection du Mur Gauche
            self.x = get_comObjs("wallLeft").x
            self.vx, self.ax = 0, 0

        if self.x + self.size >= get_comObjs("wallRight").x:        # Détection du Mur Droit
            self.x = get_comObjs("wallRight").x - self.size
            self.vx, self.ax = 0, 0
        
        for col in stage.stage0.chunks:
            for ch in col:
                if ch.state[self.num-1]:            # Vérifie si le chunk est actif (proche) pour se personnage
                    for block in ch.objs:
                        self.collide_block(block, other)        # Appelle de la fontion des calculs de collision avec les blocs statiques

        self.collide_hero_2(other)        # Seconds calculs après des collisions 

        get_can().coords(self.shape, self.x, self.y,         # Les calculs sont finis, on change les coordonées
                                 self.x + self.size, self.y + self.size)


def init(co1, co2):
    global hero1, hero2
    hero1 = Hero(1, co1[0], co1[1], "#de3193", ["Right", "Left", "Up"]) # Création du carré bleu/violet "#007FD3"
    hero2 = Hero(2, co2[0], co2[1], "#ff8a29", ["d", "q", "z"]) # Création du carré orange "#E69A00"
    # Les 2 carrés sont des objets indépendants de type (class) : Hero, donc ils ont les memes attributs (variables)
    # et les mêmes fonctions tout en marchant indépendament (en bougeant les coordonées de l'un, l'autre ne bouge pas)

def get_can():
    return window.root.canvas

def get_ratio():
    return window.root.ratio

def get_keys():
    return controls.keys

def get_comObjs(name):
    return stage.stage0.objs["Common"][name]
