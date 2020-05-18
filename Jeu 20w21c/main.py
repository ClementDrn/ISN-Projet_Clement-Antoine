''' Voici le module principal '''

import hero                     # On importe tous les modules nécessaires dans cette fenêtre
import stage
import debug
import music
import graphics
import window
import controls
from time import time


def get_can():
    return window.root.canvas

def get_win():
    return window.root.window

def main_loop():        # Boucle principale exécutée à chaque frame
    t0 = time()

    get_can().update()         # Mise à jour de l'affichage

    for obj in stage.stage0.objs["Platform"]:
        stage.stage0.objs["Platform"][obj].move()
        
    if hero.hero1.y < hero.hero2.y:         # Car le carré du dessous a plus d'influence sur le carré du dessus qu'inversement
        hero.hero2.move()       
        hero.hero1.move()
    else:
        hero.hero1.move()       # Méthodes des deux personnages leur permettant de bouger
        hero.hero2.move()

    for col in stage.stage0.chunks:
        for ch in col:
            ch.calculate()
    
    count = 0
    for key in stage.stage0.objs["Win"]:
        count += 1
        if stage.stage0.objs["Win"][key].test():
            count -= 1
    if count == 0:
        stage.stage_end()

    graphics.set_graphics()
    debug.debugger.fps_add()
    
    t0Copy = t0
    t1 = time()
    afterTime = int((wantedTimeGap - t1 + t0Copy) * 1000 + 0.4)         # +0.4 → int(x + 0.5) fait un arrondi, et -0.1 car il y a un petit temps mis pour faire les calculs du temps

    get_can().after(afterTime, main_loop)     # Appelle de nouveau la fonction [afterTime] (en ms) plus tard


# INITIALISATION du Tk et du Canvas (Tkinter)
window.init()

# Affichage du canvas
get_can().pack()

# Création des éléments principaux
hero.init((200, 400), (200, 400))       # Les personnages

stage.create(0, hero.hero1, hero.hero2)         # Le niveau 0 (provisoire)
stage.stage0.display()

for h in hero.hero1, hero.hero2:            # Affiche les carrés devant tout le reste (au cas où)
    h.display()
    get_can().tag_raise(h.shape)
for key in stage.stage0.objs["Win"]:
    get_can().tag_raise(stage.stage0.objs["Win"][key].shape)

graphics.init()                                 # Les bonus graphiques
controls.init(get_can(), hero.hero1, hero.hero2)        # Les contrôles

debug.init()

timeGap = 9
wantedTimeGap = 1 / 80          # 1 seconde divisé par le nombre de fps voulu

try:
    music.init()
    music.play_music()
except:
    print("Error: No music available")

#───────────────────────────┐
main_loop()      # La boucle principale est appelée ↑↑↑
#───────────────────────────┘

get_win().mainloop()
