''' Voici le module définissant les personnages et ce qui s'y rapportent '''

import window               # On importe les sous fichiers dont on aura besoin
import controls
import stage
import music
import debug



class Hero:         # C'est la classe des carrés
    def __init__(self, num, c, co):      # __init__ est exécuté à la création d'un objet (carré), "self" est obligatoire laisse tomber
        self.num = num
        self.x = 0         # Valeurs provisoires (x, y)
        self.y = 0
        self.oldX, self.oldY = self.x, self.y
        self.size = 50
        self.color = c
        self.ax, self.ay = 0, 0.075        # Accélération (les physiques ne fonctionnent pas avec des forces mais juste des accélérations)
        self.vx, self.vy = 0, 0                 # Vitesse
        self.controls = {"droite": co[0], "gauche": co[1], "saut": co[2]}       # Touches (inputs)
        self.onFloor = False
        self.onBlock = []
        self.onPlatform = False
        self.heroCollisionY = 3         # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "y supérieur à l'autre", 3 = autres conditions

    def display(self):
        self.shape = get_can().create_rectangle(self.x*get_ratio()+get_oX(), self.y*get_ratio()+get_oY(),                                 # Création du carré graphiquement
                                            (self.x+self.size)*get_ratio()+get_oX(), (self.y+self.size)*get_ratio()+get_oY(),     # L'origine du carré est sur le sommet en haut à droite
                                            fill = self.color, width = 0)
    
    def p_droite(self, event):                  # La touche est pressée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant VRAI
        if not debug.debugger.stop:
            get_keys()[self.controls["droite"]] = True

    def p_gauche(self, event):                  # La touche est pressée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant VRAI
        if not debug.debugger.stop:
            get_keys()[self.controls["gauche"]] = True

    def r_droite(self, event):                  # La touche est relachée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant FAUX
        if not debug.debugger.stop:
            get_keys()[self.controls["droite"]] = False

    def r_gauche(self, event):                  # La touche est relachée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant FAUX
        if not debug.debugger.stop:
            get_keys()[self.controls["gauche"]] = False

    def p_saut(self, event):                    # La touche est pressée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant VRAI
        if not debug.debugger.stop:
            if not get_keys()[self.controls["saut"]] and (self.onFloor or self.heroCollisionY == 1): # Pour sauter une seule fois jusqu'à toucher le sol
                # self.vy = -2 if self.heroCollisionY == 0 else -2.9                  
                self.vy = -2.9              # Accélération vers le haut : le saut
                self.onFloor = False            # On a décollé du sol
                # get_keys()[self.controls["saut"]] = False
                try:
                    music.jump()
                except:
                    pass
                if self.heroCollisionY == 1:       
                    self.heroCollisionY = 2      # 0 = "porte l'autre carré", 1 = "posé sur l'autre carré", 2 = "'y' supérieur à l'autre", 3 = autres conditions
                    self.get_other().heroCollisionY = 3
                    self.ay, self.get_other().ay = 0.075, 0.075
                get_keys()[self.controls["saut"]] = True

    def r_saut(self, event):                    # La touche est relachée, donc la valeur qui y corrrespond dans le dictionnaire est maintenant FAUX
        if not debug.debugger.stop:
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
            if self.y + self.size <= other.y:     # Si le bas du carré est au-dessus de l'autre..
                self.heroCollisionY = 2         
                # print("#2")
            elif self.heroCollisionY == 2:      # Est-ce que juste avant le carré qui tombe était au dessus de l'autre ??
                try:            # Pour éviter les divisions par 0
                    ratio = (self.y - self.oldY) / (other.y - self.oldY - self.size)        # Thalès pour trouver le point de collision en x
                    heroCollisionX = (self.x - self.oldX) / ratio + self.oldX
                except:
                    heroCollisionX = self.x
                if heroCollisionX > other.x - self.size and heroCollisionX < other.x + self.size:
                    self.heroCollisionY = 1             # Il s'est posé sur l'autre carré au moment de la collision
                    # print("#1")
                else:
                    self.heroCollisionY = 3             # Il est passé à côté
                    # print("#3")
            if self.heroCollisionY == 1:            # Comme il s'est posé sur l'autre, on met les bonnes coordonées et la bonne vitesse
                if not other.onFloor and self.vy > 0:
                    other.vy += self.vy * 0.3
                self.onFloor = False        # Dans le cas d'une plateforme qui descend et dépose le carré sur l'autre, il n'est plus sur du sol (sur plateforme)
                self.y = other.y - other.size
                self.ay, other.ay = 0.15, 0.15
                self.vy = other.vy
                other.heroCollisionY = 0

        else:
            if self.y + self.size < other.y:     # Si le bas du carré est au-dessus de l'autre..
                self.heroCollisionY = 2
            
    def collide_hero_2(self, other):
        if self.heroCollisionY == 1:        # Si le hero était sur l'autre...
            if self.onFloor:                # ..et que maintenant il s'est posé sur le sol (arrive si un bloc fait obstacle entre les 2 heros)
                self.heroCollisionY, other.heroCollisionY = 2, 3        # ..Alors on rectifie :
                self.ay, other.ay = 0.075, 0.075

    def collide_block(self, block, other, platDy=0):
        isImpact = False        # Pour la méthode collide_platform()
        if block.state == "solid":      # SOLID
            if self.x + self.size > block.x and self.x < block.x + block.sizeX:
                if self.y + self.size > block.y and self.y < block.y + block.sizeY:
                    if self.oldY + self.size <= block.y:              # hero provient d'en haut ?
                        self.y = block.y - self.size
                        self.onBlock[block.num], self.onFloor = True, True         # L'avantage d'utiliser onBlock en plus : il ne peut être changé qu'ici contrairement à onFloor, donc on peut tester si avant le hero était sur le block
                        self.vy = 0
                    elif self.oldY >= block.y + block.sizeY:      # hero provient d'en bas ?
                        self.y = block.y + block.sizeY + (block.y + block.sizeY - self.y) / 4
                        self.vy *= -0.5
                        self.onFloor = False
                        if self.heroCollisionY == 1:
                            other.y = block.y + block.sizeY + (block.y + block.sizeY - self.y) / 4 + self.size
                            other.vy *= -0.5
                            if other.onPlatform:
                                other.onFloor = False
                            self.change(other)
                        # elif (other.y - block.y - block.sizeY >= self.size) and (self.y > other.y - self.size):      
                        #     self.y = other.y - self.size        # Quand il y a juste la place entre l'autre carré et le plafond
                        #     self.vy = 0
                        #     self.heroCollisionY, other.heroCollisionY = 1, 0
                    elif self.oldX + self.size <= block.x:              # hero provient de la gauche ?
                        dist = self.x + self.size - block.x
                        # self.x = block.x - self.size
                        self.x -= dist
                        self.ax, self.vx = 0, 0
                    elif self.oldX >= block.x + block.sizeX:      # hero provient de la droite ?
                        dist = block.x + block.sizeX - self.x
                        self.x += dist
                        self.ax, self.vx = 0, 0
                elif self.onBlock[block.num] and self.vy != 0:
                    self.onBlock[block.num], self.onFloor = False, False
            elif self.onBlock[block.num]:
                self.onBlock[block.num], self.onFloor = False, False
# SEMI-SOLID
        elif block.y <= self.y + self.size and self.vy >= platDy / 2:    # Si le hero passe..
            # if (get_can().coords(self.shape)[3]-get_oY())/get_ratio() <= block.y:      #..à travers le bloc
            if self.oldY + self.size <= block.y - platDy:    # - platDy * 2
                try:
                    ratio = (self.y - self.oldY) / (block.y - self.oldY - self.size)        # Thalès pour trouver le point de collision en x
                    collisionX = (self.x - self.oldX) / ratio + self.oldX
                except:         # Division par 0
                    collisionX = self.x
                    # print("except")
                if block.x < collisionX + self.size and collisionX < block.x + block.sizeX:       # La collision a eu lieu
                    self.y = block.y - self.size
                    self.onBlock[block.num], self.onFloor = True, True
                    self.vy = 0
                    isImpact = True         # L'impact a eu lieu
            if not (self.x + self.size > block.x and self.x < block.x + block.sizeX) and self.onBlock[block.num]:   # S'il sort de.. 
                self.onBlock[block.num], self.onFloor = False, False                                #.. l'intervalle de collision en X
        elif self.onBlock[block.num] and self.vy != 0:      # Le hero s'est fait déplacé (typiquement, l'autre le pousse vers le haut)
            self.onBlock[block.num], self.onFloor = False, False
        return isImpact         # Sert uniquement dans le cas d'une plateforme

    def collide_platform(self, platform, other):
        if self.collide_block(platform.block, other, platform.dy):
        # if self.onBlock[platform.block.num] or self.collide_block(platform.block, other, True):
        # if self.onBlock[platform.block.num]:
        #     if self.heroCollisionY == 1 or not (self.x + self.size > platform.block.x and self.x < platform.block.x + platform.block.sizeX):
        #         self.onBlock[platform.block.num] = False
        # elif self.collide_block(platform.block, other, True):
            self.vx += platform.dx / 2          # Divisé par 2 car le déplacement des carrés est toujours *2 contrairement aux plateformes qui sont *1
            self.vy = platform.dy / 2
            self.x = self.oldX + self.vx * 2
            # self.y = self.oldY + self.vy * 2
            # self.y += platform.dy / 2
            self.onPlatform = True
            if self.heroCollisionY == 0:
                other.vx += self.vx
                # other.vy += self.vy
            
    
    def change(self, other):
        get_can().coords(other.shape, other.x*get_ratio()+get_oX(), other.y*get_ratio()+get_oY(),         # Les calculs sont finis, on change les coordonées
                                (other.x+other.size)*get_ratio()+get_oX(), (other.y+other.size)*get_ratio()+get_oY())

    def move(self):                 # Méthode pour bouger les personnages
        self.onPlatform = False
        self.oldX, self.oldY = self.x, self.y       # La position actuelle avant de bouger
        self.set_vy()
        self.set_vx()
        other = self.get_other()
        if self.heroCollisionY == 1:
            self.vx += other.vx
        self.x += self.vx * 2           # Projection des futures coordonées
        self.y += self.vy * 2

        self.collide_hero(other)      # On teste si le hero est le hero1, et en méthode on appelle une méthode avec pas les attributs de l'autre carré
        
        for key in stage.stage0.objs["Platform"]:
            plat = stage.stage0.objs["Platform"][key]
            self.collide_platform(plat, other)
        
        if self.y <= get_comObjs("ceiling").y:          # Détection du Plafond
            self.y = get_comObjs("ceiling").y + (get_comObjs("ceiling").y - self.y) / 4     # La distance au dessus du plafond est mise en dessous (/2), mais est + petite dû à l'élasticité (/2)
            self.vy *= -0.5     # Elasticité
            self.onFloor = False
            if self.heroCollisionY == 1:        # Si il est porté, l'autre doit rebondir aussi
                other.y = get_comObjs("ceiling").y + (get_comObjs("ceiling").y - self.y) / 4 + self.size
                other.vy *= -0.5
                if other.onPlatform:
                    other.onFloor = False
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
            dist = get_comObjs("wallLeft").x - self.x
            self.x += dist
            self.vx, self.ax = 0, 0

        if self.x + self.size >= get_comObjs("wallRight").x:        # Détection du Mur Droit
            dist = self.x + self.size - get_comObjs("wallRight").x
            self.x -= dist
            self.vx, self.ax = 0, 0
        
        for col in stage.stage0.chunks:
            for ch in col:
                if ch.state[self.num-1]:            # Vérifie si le chunk est actif (proche) pour se personnage
                    for block in ch.objs:
                        self.collide_block(block, other)        # Appelle de la fontion des calculs de collision avec les blocs statiques

        self.collide_hero_2(other)        # Seconds calculs après des collisions

        get_can().coords(self.shape, self.x*get_ratio()+get_oX(), self.y*get_ratio()+get_oY(),         # Les calculs sont finis, on change les coordonées
                                (self.x+self.size)*get_ratio()+get_oX(), (self.y+self.size)*get_ratio()+get_oY())


def init():
    global hero1, hero2
    hero1 = Hero(1, "#de3193", ["d", "q", "z"]) # Création du carré bleu/violet "#007FD3"
    hero2 = Hero(2, "#ff8a29", ["Right", "Left", "Up"]) # Création du carré orange "#E69A00"
    # Les 2 carrés sont des objets indépendants de type (class) : Hero, donc ils ont les memes attributs (variables)
    # et les mêmes fonctions tout en marchant indépendament (en bougeant les coordonées de l'un, l'autre ne bouge pas)

def get_can():
    return window.root.canvas

def get_ratio():
    return window.root.ratio

def get_oX():
    return window.root.oX

def get_oY():
    return window.root.oY

def get_keys():
    return controls.keys

def get_comObjs(name):
    return stage.stage0.objs["Common"][name]
