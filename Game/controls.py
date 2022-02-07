'''Voici le module s'occupant de tout ce qui est des contrôles/inputs'''

from Game import debug
from Game import window


keys = None

def init(canvas, hero1, hero2):
    global keys         # Dictionnaire des touches, indiquant si celles-ci sont pressées ou non
    keys = {'d': False, 'q': False, 'z': False, "Left": False, "Right": False, "Up": False}

    # Dans cette partie du programme, on assimile les ordres donnés par le programme à une touche du clavier
    canvas.bind_all('<Right>', hero2.p_droite)      # la flêche directionnel de droite sur le clavier est assimilé au mouvement droite du hero1
    canvas.bind_all('<KeyRelease-Right>', hero2.r_droite)       # quand on arrête d'appuyer sur la touche le héro ne bouge plus 
    canvas.bind_all('<Left>', hero2.p_gauche)       #la flêche directionnel de gauche sur le clavier est assimilé au mouvement gauche du hero1
    canvas.bind_all('<KeyRelease-Left>', hero2.r_gauche)        # quand on arrête d'appuyer sur la touche le héro ne bouge plus 
    canvas.bind_all('<Up>', hero2.p_saut)           #la flêche directionnel du haut sur le clavier est assimilé au mouvement saut du hero1 
    canvas.bind_all('<KeyRelease-Up>', hero2.r_saut)            # quand on arrête d'appuyer sur la touche le héro ne bouge plus 

    canvas.bind_all('<d>', hero1.p_droite)          # De même ave le héro2 mais avec les touches z;q;d
    canvas.bind_all('<KeyRelease-d>', hero1.r_droite)
    canvas.bind_all('<q>', hero1.p_gauche)
    canvas.bind_all('<KeyRelease-q>', hero1.r_gauche)
    canvas.bind_all('<z>', hero1.p_saut)
    canvas.bind_all('<KeyRelease-z>', hero1.r_saut)

    canvas.bind_all('<Return>', debug.debugger.debug_enter)         # Pour rentrer des commandes
    canvas.bind_all('<Escape>', window.root.quit_game)              # Quitte le jeu
