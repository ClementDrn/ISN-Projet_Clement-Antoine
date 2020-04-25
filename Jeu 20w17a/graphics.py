''' Voici le module qui s'occupe des "bonus" graphiques (pour le swag) '''

import window
import hero


def init():
    global hTransparency        # C'est le rectangle (rouge actuellement), qui vient s'ajouter là où les deux carrés se superposent
    hTransparency = window.root.canvas.create_rectangle(-1, -1, -1, -1, fill="#ff2e2e", width=0)        # rouge/vert:"#55ff5f"

def get_can():                  # Pour éviter une longue ligne de code
    return window.root.canvas

def red_coords(hero1, hero2):           # Fonction pour calculer l'intervalle en 2 dimensions de l'endroit où les 2 carrés se superposent

    if (hero1.y > hero2.y - hero2.size and hero1.y < hero2.y + hero2.size) and (
    hero1.x > hero2.x - hero2.size and hero1.x < hero2.x + hero2.size):
        x3 = [hero1.x, hero2.x + hero2.size] if hero1.x > hero2.x else [hero2.x, hero1.x + hero1.size]
        y3 = [hero1.y, hero2.y + hero2.size] if hero1.y > hero2.y else [hero2.y, hero1.y + hero1.size]
        return (x3[0], y3[0], x3[1], y3[1])     # Retourne les valeurs
    else:
        return (-1, -1, -1, -1)                 # Si les carrés ne se superposent pas alors, on positionne hTransparency hors champ

def set_graphics():             # Fonction pour actualiser les éléments graphiques
    coords3 = red_coords(hero.hero1, hero.hero2)
    get_can().coords(hTransparency, coords3[0], coords3[1], coords3[2], coords3[3])
