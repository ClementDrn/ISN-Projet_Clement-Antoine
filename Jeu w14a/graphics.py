import window


def init():
    global hTransparency
    hTransparency = window.root.canvas.create_rectangle(-1, -1, -1, -1, fill="#ff2e2e", width=0)        # rouge/vert:"#55ff5f"

def redCoords(hero1, hero2):
    if (hero1.y > hero2.y - hero2.size and hero1.y < hero2.y + hero2.size) and (hero1.x > hero2.x - hero2.size and hero1.x < hero2.x + hero2.size):
        x3 = [hero1.x, hero2.x + hero2.size] if hero1.x > hero2.x else [hero2.x, hero1.x + hero1.size]
        y3 = [hero1.y, hero2.y + hero2.size] if hero1.y > hero2.y else [hero2.y, hero1.y + hero1.size]
        return (x3[0], y3[0], x3[1], y3[1])
    else:
        return (-1, -1, -1, -1)

