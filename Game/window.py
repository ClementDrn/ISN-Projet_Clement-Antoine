'''Voici le module qui définit le Tk et le Canvas'''

import tkinter as tk


root = None

class Root:
    def __init__(self, c):
        # Création de la fenêtre et du canvas(pour faire des "dessins" de carrés et autres)
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)         # Plein écran
        self.screenW = self.window.winfo_screenwidth()
        self.screenH = self.window.winfo_screenheight()
        print(self.screenW, self.screenH)
        self.bg = c
        self.winH, self.winW = 0, 0         # Modifiés plus tard
        self.oX, self.oY = 0, 0
        self.shape = None
        self.canvas = tk.Canvas(height=self.screenH, width=self.screenW, background=self.bg, bd=0)

    def calibrate(self, h, w):              # Calibre la taille du niveau à affiché avec la taille de l'écran
        ratioY = self.screenH / h
        ratioX = self.screenW / w

        self.ratio = ratioY if ratioY < ratioX else ratioX
        self.winH = h
        self.winW = w
        self.oX = int((self.screenW - w * self.ratio) / 2 + 0.5)
        self.oY = int((self.screenH - h * self.ratio) / 2 + 0.5)
        print(self.oX, self.oY)
        print("ratio", self.ratio)
        print("window", self.winH, self.winW)

    def quit_game(self, event):
        self.window.destroy()


def init():         # Créer une instance de la classe Root
    global root
    root = Root("white")
