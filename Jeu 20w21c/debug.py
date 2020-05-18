''' Voici le module qui a une fonction de déboggage '''

import window
# import stage
# import hero


class Debug:
    def __init__(self):
        self.fps = 0

    def fps_add(self):
        self.fps += 1

    def fps_reset(self):
        print(self.fps)
        self.fps = 0
        get_can().after(1000, self.fps_reset)

'''
def debug_enter(event):             # /!\ Il ne faut pas écrire n'importe quoi par mesure de sécurité, par exemple : func effacer_tout_les_fichiers()
    command = input("Command > ")
    words = command.split()
    
    if words:
        if words[0] == "help":
            print("-----------------------------------------------")
            # print("* func <function>\n    Pour appeller une fonction\n* var <name> <value> <int|float|str> [instance]\n    Pour changer la valeur d'une variable")
            print("* level <number>\n    Pour lancer un niveau\n* var <name> <value> <int|float|str> [instance]\n    Pour changer la valeur d'une variable")
            print("-----------------------------------------------")

        # elif words[0] == "func":          # func <function>
        #     eval(words[1])
        #     print("The function", words[1], "has been executed")

        elif words[0] == "level":
            stage.create(int(words[1]), hero.hero1, hero.hero2) 
        
        elif words[0] == "var":         # var <name> <value> <int|float|str> [instance]
            if len(words) == 5:
                if words[3] == "int":
                    setattr(eval(words[4]), words[1], int(words[2]))
                elif words[3] == "float":
                    setattr(eval(words[4]), words[1], float(words[2]))
                elif words[3] == "str":
                    setattr(eval(words[4]), words[1], words[2])
                print(words[4] + '.' + words[1], "is now equal to", words[2])

            elif len(words) == 4:
                if words[3] == "int":
                    globals()[words[1]] = int(words[2])
                elif words[3] == "float":
                    globals()[words[1]] = float(words[2])
                elif words[3] == "str":
                    globals()[words[1]] = words[2]
                print(words[1], "is now equal to", words[2])
'''

def init():
    global debugger
    debugger = Debug()
    debugger.fps_reset()

def get_can():
    return window.root.canvas

def get_winH():
    return window.root.winH

def get_winW():
    return window.root.winW

def round_num(number):          # Arrondi tout à la valeur du dessous pour éviter les erreurs dû aux arrondi parfois au-dessus puis au-dessous
    return int(number*1000)/1000        # ex : 1.66666666667 devient 1.666