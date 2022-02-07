'''Voici le module s'occupant des sons'''

from random import randint
from pygame import mixer
import pathlib
# from os import getcwd               # Pour obtenir le chemin d'accès du fichier actuel dans l'arborescence.

jumps, winSound = [None]*2

def init():
    mixer.pre_init(44100, -16, 2, 1024)
    mixer.init()

    path = str(pathlib.Path(__file__).parent.absolute())
    print(path)
    global jumps, winSound
    jumps = {1: None, 2: None, 3: None, 4: None, 5: None}
    for i in range(1, 6):
        jumps[i] = mixer.Sound(path + "\\sounds\\jump\\jump0" + str(i) + ".wav")
    winSound = mixer.Sound(path + "\\sounds\\end\\win.ogg")          # Son de victoire
    mixer.music.load(path + "\\sounds\\music\\theme.mp3")

def jump():         # Son du saut
    num = randint(1, 5)
    jumps[num].play()

def play_music():           # Musique
    mixer.music.play(-1)         # Joue indéfiniment
    mixer.music.set_volume(0.6)
