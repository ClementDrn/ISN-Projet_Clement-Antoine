''' Voici le module qui a une fonction de déboggage '''

import window


class Debug:
    def __init__(self):
        self.fps = 0

    def fps_add(self):
        self.fps += 1

    def fps_reset(self):
        print(self.fps)
        self.fps = 0
        get_can().after(1000, self.fps_reset)


def debug_enter(event):             # /!\ Il ne faut pas écrire n'importe quoi par mesure de sécurité, par exemple : func effacer_tout_les_fichiers()
    command = input("Command > ")
    words = command.split()
    
    if words:
        if words[0] == "help":
            print("-----------------------------------------------")
            print("* func <function>\n    Pour appeller une fonction\n* var <name> <value> <int|float|str> [instance]\n    Pour changer la valeur d'une variable")
            print("-----------------------------------------------")

        if words[0] == "func":          # func <function>
            eval(words[1])
            print("The function", words[1], "has been executed")
        
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


def init():
    global fps
    fps = Debug()
    fps.fps_reset()

def get_can():
    return window.root.canvas
