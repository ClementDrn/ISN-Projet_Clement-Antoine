from tkinter import*

class Plateforme:
    def __init__(self, x, y, c,sizeX,sizeY):
        self.x=x
        self.y=y
        self.sizeX=sizeX
        self.sizeY=sizeY

        self.color=c
        self.Plateforme = canvas.create_rectangle(self.x, self.y,                                 # Création du carré graphiquement
                                            self.x + self.sizeX, self.y + self.sizeY,         # L'origine du carré est sur le sommet en haut à droite
                                            fill = self.color, width = 0)



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

window.mainloop()