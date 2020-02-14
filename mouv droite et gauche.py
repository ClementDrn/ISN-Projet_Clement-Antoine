from tkinter import*
import time                 # Pour time.sleep() qui sert à arrêter le script pour un certain temps en secondes


class Hero:         # C'est la classe des carrés
    def __init__(self, x, y, s, c):      # __init__ est exécuté à la création d'un objet (carré), "self" est obligatoire laisse tomber
        self.x = x                       # x, y, s et c sont les attributs indiqués à la création des carrés (ligne 36)
        self.y = y                       # ensuite on défini les variables du carré grâce aux attributs
        self.size = s
        self.color = c
        self.hero = canvas.create_rectangle(self.x - self.size/2, self.y - self.size/2,     # Création du carré graphiquement
                                            self.x + self.size/2, self.y + self.size/2,
                                            fill = self.color, width = 0)

    def droite(self, event):
        canvas.move(self.hero, 2, 0)
        canvas.update()         # Mise à jour de l'affichage
    def gauche(self,event):
        canvas.move(self.hero,-2,0)



# Variables de la fenêtre "window"
winH = 540
winW = 960
bg = "white"

# Création de la fenêtre et du canvas(pour faire des "dessins" de carrés et autres)
window = Tk()
canvas = Canvas(height=winH, width=winW, background=bg)

# Affichage du canvas
canvas.pack()


hero1 = Hero(500, 400, 50, "#007FD3") # Création du carré bleu
hero2 = Hero(200, 400, 50, "#E69A00") # Création du carré orange
# Les 2 carrés sont des objets indépendants de type (class) : Hero, donc ils ont les memes attributs (variables)
# et les mêmes fonctions tout en marchant indépendament (en bougeant les coordonées de l'un, l'autre ne bouge pas)


canvas.bind_all('<Right>', hero1.droite)
canvas.bind_all('<Left>',hero1.gauche)

canvas.bind_all('<d>', hero2.droite)
canvas.bind_all('<q>',hero2.gauche)


'''
# Démonstration (boucle infini) du déplacement des carrés
while 1:
    for i in range(100):
        hero1.move(-2, 0)
        hero2.move(1, -2)
        time.sleep(1/60)            # Pour voir les changements, correspond à (1sec / 60), donc un peu moins
                                    # de 60fps (car il y a aussi le temps d'exécution du script)
    for i in range(100):
        hero1.move(2, 0)
        hero2.move(-1, 2)
        time.sleep(1/60)
'''

window.mainloop()