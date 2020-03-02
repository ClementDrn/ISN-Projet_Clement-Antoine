from tkinter import*
import time                 # (non utilisé)


class Hero:         # C'est la classe des carrés
    def __init__(self, x, y, s, c, co):      # __init__ est exécuté à la création d'un objet (carré), "self" est obligatoire laisse tomber
        self.x = x                       # x, y, s et c sont les attributs indiqués à la création des carrés (ligne 36)
        self.y = y                       # ensuite on défini les variables du carré grâce aux attributs
        self.size = s
        self.color = c
        self.hero = canvas.create_rectangle(self.x - self.size/2, self.y - self.size/2,     # Création du carré graphiquement
                                            self.x + self.size/2, self.y + self.size/2,
                                            fill = self.color, width = 0)
        self.ax, self.ay = 0, 0.07
        self.vx, self.vy = 0, 0
        self.controls = {"droite": co[0], "gauche": co[1], "saut": co[2]}
        self.onFloor = True
    
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
        if keys[self.controls["saut"]] == False and self.onFloor == True: # Pour sauter une seule fois jusqu'à toucher le sol
            keys[self.controls["saut"]] = True
            self.vy = -3
            self.onFloor = False
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
        if self.onFloor == False:
            self.vy += self.ay          # On augmente la vitesse vers le bas grâce à l'accélération (gravité)


    def move(self):
        self.set_vy()
        self.x += self.vx * 2
        self.y += self.vy * 2
        canvas.move(self.hero, self.vx*2, self.vy*2)
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


hero1 = Hero(500, 400, 50, "#007FD3", ["Right", "Left", "Up"]) # Création du carré bleu
hero2 = Hero(200, 400, 50, "#E69A00", ["d", "q", "z"]) # Création du carré orange
# Les 2 carrés sont des objets indépendants de type (class) : Hero, donc ils ont les memes attributs (variables)
# et les mêmes fonctions tout en marchant indépendament (en bougeant les coordonées de l'un, l'autre ne bouge pas)

# Dictionnaire de l'état des touches
keys = {'d': False, 'q': False, 'z': False, "Left": False, "Right": False, "Up": False}

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


hero1.move()
hero2.move()
    

window.mainloop()
