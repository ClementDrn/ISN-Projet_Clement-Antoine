import tkinter as tk
import hero                     # On importe tous les sous fichiers dans cette fenêtre, c'est à dire les fichiers: hero,stage,debug,graphics,window
import stage
import debug
import graphics
import window


def get_can():
    return window.root.canvas

def get_win():
    return window.root.window


# INITIALISATION
window.init()



# Affichage du canvas
get_can().pack()


# Création des éléments principaux
stage.create(0)
stage.stage0.display()

hero.init((500, 400), (200, 400))

graphics.init()


# Dans cette partie du programme, on assimile les ordres donnés par le programme à une touche du clavier
get_can().bind_all('<Right>', hero.hero1.p_droite)      # la flêche directionnel de droite sur le clavier est assimilé au mouvement droite du hero1
get_can().bind_all('<KeyRelease-Right>', hero.hero1.r_droite)       # quand on arrête d'appuyer suer la touche le héro ne bouge plus 
get_can().bind_all('<Left>', hero.hero1.p_gauche)       #la flêche directionnel de gauche sur le clavier est assimilé au mouvement gauche du hero1
get_can().bind_all('<KeyRelease-Left>', hero.hero1.r_gauche)        # quand on arrête d'appuyer suer la touche le héro ne bouge plus 
get_can().bind_all('<Up>', hero.hero1.p_saut)           #la flêche directionnel du haut sur le clavier est assimilé au mouvement saut du hero1 
get_can().bind_all('<KeyRelease-Up>', hero.hero1.r_saut)            # quand on arrête d'appuyer suer la touche le héro ne bouge plus 

get_can().bind_all('<d>', hero.hero2.p_droite)          # De même ave le héro2 mais avec les touches z;q;s;d
get_can().bind_all('<KeyRelease-d>', hero.hero2.r_droite)
get_can().bind_all('<q>', hero.hero2.p_gauche)
get_can().bind_all('<KeyRelease-q>', hero.hero2.r_gauche)
get_can().bind_all('<z>', hero.hero2.p_saut)
get_can().bind_all('<KeyRelease-z>', hero.hero2.r_saut)

get_can().bind_all('<Return>', debug.debug_enter)



hero.hero1.move()
hero.hero2.move()


get_win().mainloop()
