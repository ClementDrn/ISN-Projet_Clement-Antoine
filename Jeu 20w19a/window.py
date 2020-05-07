'''Voici le module qui définit le Tk et le Canvas'''

import tkinter as tk


class Root:
    def __init__(self, h, w, c):
        # Création de la fenêtre et du canvas(pour faire des "dessins" de carrés et autres)
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True) 
        self.screenW = self.window.winfo_screenwidth()
        self.screenH = self.window.winfo_screenheight()
        print(self.screenW, self.screenH)

        ratioY = self.screenH / h
        ratioX = self.screenW / w

        self.ratio = ratioY if ratioY < ratioX else ratioX
        self.winH = h * self.ratio
        self.winW = w * self.ratio
        self.oX = (self.screenW - self.winW) / 2
        self.oY = (self.screenH - self.winH) / 2
        print(self.oX, self.oY)

        self.bg = c
        self.canvas = tk.Canvas(height=self.screenH, width=self.screenW, background=self.bg, bd=0)


def init():         # Créer une instance de la classe Root
    global root
    root = Root(540, 960, "white")
