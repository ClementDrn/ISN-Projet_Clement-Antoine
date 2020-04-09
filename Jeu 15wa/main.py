''' Voici le module principal '''

import hero                     # On importe tous les modules nécessaires dans cette fenêtre
import stage
import debug
import graphics
import window
import controls


def get_can():
    return window.root.canvas

def get_win():
    return window.root.window

def main_loop():        # Boucle principale exécutée à chaque frame
    hero.hero1.move()       
    hero.hero2.move()       # Méthodes des deux personnages leur permettant de bouger
    for obj in stage.stage0.objs["Platform"]:
        stage.stage0.objs["Platform"][obj].move()  

    graphics.set_graphics()
    debug.fps.fps_add()

    get_can().update()         # Mise à jour de l'affichage
    get_can().after(frameRate, main_loop)     # Recall de la fonction 10ms plus tard



# INITIALISATION du Tk et du Canvas (Tkinter)
window.init()

# Affichage du canvas
get_can().pack()

# Création des éléments principaux
stage.create(0)         # Le niveau 0 (provisoire)
stage.stage0.display()

hero.init((500, 400), (200, 400))       # Les personnages
graphics.init()                                 # Les bonus graphiques
controls.init(get_can(), hero.hero1, hero.hero2)        # Les contrôles

debug.init()

frameRate = 9

#────────────────┐
main_loop()      # La boucle principale est appelée ↑↑
#────────────────┘

get_win().mainloop()
