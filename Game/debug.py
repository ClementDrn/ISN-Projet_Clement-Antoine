''' Voici le module qui a une fonction de déboggage '''

from Game import window
import time


debugger = None

class Debug:
    def __init__(self, stage):
        self.fps = 0
        self.t0Win = 0
        self.stage = stage
        self.stop = False

    def fps_add(self):      # Compteur de fps
        self.fps += 1

    def fps_reset(self):
        if not self.stop:
            print(self.fps)
        self.fps = 0
        get_can().after(1000, self.fps_reset)

    def debug_enter(self, event):             # Pour entre des commandes
        if not self.stop:
            self.stop = True
            command = input("Command > ")
            words = command.split()
            
            if words:
                if words[0] == "help":
                    print("-----------------------------------------------")
                    # print("* func <function>\n    Pour appeller une fonction\n* var <name> <value> <int|float|str> [instance]\n    Pour changer la valeur d'une variable")
                    print("* level <number>\n    Pour lancer un niveau\n* finish\n    Pour automatiquement finir le niveau")
                    print("-----------------------------------------------")

                elif words[0] == "level":
                    self.stage.change_level(int(words[1])) 

                elif words[0] == "finish":
                    self.t0Win = self.stage.stage_end()
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
