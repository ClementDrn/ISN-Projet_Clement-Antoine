''' Voici le module principal '''

import hero                     # On importe tous les modules nécessaires dans cette fenêtre
import stage
import debug
import music
import graphics
import window
import controls
import time
from threading import Thread


def get_can():
    return window.root.canvas

def get_win():
    return window.root.window

def main_loop():        # Boucle principale exécutée à chaque frame
    t0 = time.time()
    global timeInWinArea

    if not debug.debugger.stop:
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
        
        count1 = 0
        for key in stage.stage0.objs["Win"]:
            count1 += 1
            if stage.stage0.objs["Win"][key].test():
                count1 -= 1
        if count1 == 0:
            timeInWinArea += 1
            if timeInWinArea == 80:
                global t0Win
                t0Win = stage.stage_end()
        else:
            timeInWinArea = 0

        graphics.set_graphics()
        debug.debugger.fps_add()
        

    t1 = time.time()
    if stage.hasWon and t1 - t0Win > 3:
        stage.hasWon = False
        stage.change_level(stage.stage0.level+1)
    afterTime = int((wantedTimeGap - t1 + t0) * 1000 + 0.4)         # +0.4 → int(x + 0.5) fait un arrondi, et -0.1 car il y a un petit temps mis pour faire les calculs du temps
    # print(timeInWinArea)
    get_can().after(afterTime, main_loop)     # Appelle de nouveau la fonction [afterTime] (en ms) plus tard


# INITIALISATION du Tk et du Canvas (Tkinter)
window.init()

# Affichage du canvas
get_can().pack()

debug.init(stage)

# Création des éléments principaux
hero.init()       # Les personnages
stage.init(hero.hero1, hero.hero2)

stage.change_level(1)         # Le niveau 1

controls.init(get_can(), hero.hero1, hero.hero2)        # Les contrôles

framerate = 80
wantedTimeGap = 1 / framerate          # 1 seconde divisé par le nombre de fps voulu
global timeInWinArea, t0Win
t0Win = 0

try:
    music.init()
    music.play_music()
except:
    print("Error: No music available")

#───────────────────────────┐
main_loop()      # La boucle principale est appelée ↑↑↑
#───────────────────────────┘

get_win().mainloop()
