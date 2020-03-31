import tkinter as tk


class Root:
    def __init__(self, h, w, c):
        # Variables de la fenêtre "window"
        self.winH = h
        self.winW = w
        self.bg = c

        # Création de la fenêtre et du canvas(pour faire des "dessins" de carrés et autres)
        self.window = tk.Tk()
        self.canvas = tk.Canvas(height=self.winH, width=self.winW, background=self.bg)



def init():
    global root
    root = Root(540, 960, "white")

