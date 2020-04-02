from tkinter import*


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
        self.dx=1
        self.dy=-1

    def move(self):
        self.move_update()
        canvas.move(self.Plateforme, self.dx, self.dy)
        canvas.update()
        canvas.after(10, self.move)

    def move_update(self):

         x1,y1,x2,y2= canvas.coords(self.Plateforme)
         print('coords:',x1,y1,x1,y2)

         global dx
         global dy

         if x1<0 or x2 > 540:
            self.dx*=-1
         if y1  == 0 or y2 >540:
            self.dy*=-1


# Variables de la fenêtre "window"
winH = 540
winW = 960
bg = "white"


 # Création de la fenêtre et du canvas(pour faire des "dessins" de carrés et autres)
window = Tk()
canvas = Canvas(height=winH, width=winW, background=bg)


# Affichage du canvas
canvas.pack()

plateforme= Plateforme(200, 200, "#007FD3",120,10)
plateforme2=Plateforme(50,0,"#007FD3",120,10)
plateforme3= Plateforme(800, 40, "#007FD3",120,10)


plateforme2.move()
plateforme.move()
plateforme3.move()



window.mainloop()