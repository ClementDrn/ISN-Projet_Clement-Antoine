''' Voici le module principal '''

import hero                     # On importe tous les modules nécessaires dans cette fenêtre
import stage
import debug
import music
import graphics
import window
import controls


def get_can():
    return window.root.canvas

def get_win():
    return window.root.window

def main_loop():        # Boucle principale exécutée à chaque frame
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

    graphics.set_graphics()
    debug.debuger.fps_add()
    # print(hero.hero1.onBlock)
    
    count = 0
    for key in stage.stage0.objs["Win"]:
        count += 1
        if stage.stage0.objs["Win"][key].test():
            count -= 1
    if count == 0:
        stage.stage_end()

    get_can().update()         # Mise à jour de l'affichage
    get_can().after(frameRate, main_loop)     # Recall de la fonction 10ms plus tard


# INITIALISATION du Tk et du Canvas (Tkinter)
window.init()

# Affichage du canvas
get_can().pack()

# Création des éléments principaux
hero.init((200, 400), (200, 400))       # Les personnages

stage.create(1, hero.hero1, hero.hero2)         # Le niveau 0 (provisoire)
stage.stage0.display()

for h in hero.hero1, hero.hero2:            # Affiche les carrés devant tout le reste (au cas où)
    h.display()
    get_can().tag_raise(h.shape)
for key in stage.stage0.objs["Win"]:
    get_can().tag_raise(stage.stage0.objs["Win"][key].shape)

graphics.init()                                 # Les bonus graphiques
controls.init(get_can(), hero.hero1, hero.hero2)        # Les contrôles

debug.init()

frameRate = 9

try:
    music.init()
    music.play_music()
except:
    print("Error: No music available")

#────────────────┐
main_loop()      # La boucle principale est appelée ↑↑↑
#────────────────┘

get_win().mainloop()
