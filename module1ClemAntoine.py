from tkinter import*
import time

class Plateforme:
    def __init__(self, x, y, c,sizeX,sizeY,):
        self.x=x
        self.y=y
        self.sizeX=sizeX
        self.sizeY=sizeY

        self.color=c
        self.Plateforme = canvas.create_rectangle(self.x, self.y,                                 # Création du carré graphiquement
                                            self.x + self.sizeX, self.y + self.sizeY,         # L'origine du carré est sur le sommet en haut à droite
                                            fill = self.color, width = 0)
                                            
    def move(self):
        self.move_update()
        canvas.move(self.Plateforme, dx, dy)
        canvas.update()
        canvas.after(10, self.move)

    def move_update(self):
        global dx
        global dy
        dx = 1
        dy = 1





# Variables de la fenêtre "window"
winH = 540
winW = 960
bg = "white"


 # Création de la fenêtre et du canvas(pour faire des "dessins" de carrés et autres)
window = Tk()
canvas = Canvas(height=winH, width=winW, background=bg)


# Affichage du canvas
canvas.pack()

plateforme= Plateforme(500, 200, "#007FD3",120,10)
plateforme2=Plateforme(700,150,"#007FD3",120,10)



plateforme.move()

'''
while 1:
    for i in range(100):
        # plateforme.move(-2, 0)
        # plateforme2.move(0, -2)
        canvas.move(plateforme.Plateforme, -2, 0)
        time.sleep(1/60)            # Pour voir les changements, correspond à (1sec / 60), donc un peu moins
                                    # de 60fps (car il y a aussi le temps d'exécution du script)
        canvas.update()
    for i in range(100):
        # plateforme.move(2, 0)
        # plateforme2.move(plateforme,-1, 2)
        time.sleep(1/60)
        canvas.update()
'''


window.mainloop()
