from tkinter import *

#Une fonction pour le deplacement vers la droite :
def droite(event):
    canvas.move(carré,10,0)

#On cree une fenêtre et un canevas:
tk = Tk()
canvas = Canvas(tk,width = 1000, height = 500 , bd=0, bg="white")
canvas.pack(padx=10,pady=10)

#Création  d'un bouton "Quitter" pour que quand on arruive au bout on puisse quitter;
Bouton_Quitter=Button(tk, text ='Quitter', command = tk.destroy)

Bouton_Quitter.pack()

#On cree le carré
carré = canvas.create_rectangle(300,380,300,380,fill='red')

#On associe la touche droite du clavier a la fonction droite():
canvas.bind_all('<Right>', droite)

#On lance la boucle principale:
tk.mainloop()