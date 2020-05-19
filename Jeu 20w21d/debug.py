''' Voici le module qui a une fonction de déboggage '''

import window
import time
# import stage
# import hero


class Debug:
    def __init__(self, stage):
        self.fps = 0
        self.stage = stage
        self.stop = False

    def fps_add(self):
        self.fps += 1

    def fps_reset(self):
        if not self.stop:
            print(self.fps)
        self.fps = 0
        get_can().after(1000, self.fps_reset)

    def wait(self, t):
        time.sleep

    def debug_enter(self, event):             # /!\ Il ne faut pas écrire n'importe quoi par mesure de sécurité, par exemple : func effacer_tout_les_fichiers()
        if not self.stop:
            self.stop = True
            command = input("Command > ")
            words = command.split()
            
            if words:
                if words[0] == "help":
                    print("-----------------------------------------------")
                    # print("* func <function>\n    Pour appeller une fonction\n* var <name> <value> <int|float|str> [instance]\n    Pour changer la valeur d'une variable")
                    print("* level <number>\n    Pour lancer un niveau")
                    print("-----------------------------------------------")

                elif words[0] == "level":
                    self.stage.change_level(int(words[1])) 
            self.stop = False


def init(stage):
    global debugger
    debugger = Debug(stage)
    debugger.fps_reset()

def get_can():
    return window.root.canvas

def get_winH():
    return window.root.winH

def get_winW():
    return window.root.winW
