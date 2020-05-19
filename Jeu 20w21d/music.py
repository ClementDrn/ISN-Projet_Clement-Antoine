'''Voici le module s'occupant des sons'''

from random import randint
from pygame import mixer


def init():
    mixer.pre_init(44100, -16, 2, 1024)
    mixer.init()

    global jumps
    jumps = {1: None, 2: None, 3: None, 4: None, 5: None}
    for i in range(1, 6):
        jumps[i] = mixer.Sound("sounds\\jump\\jump0" + str(i) + ".wav")
    mixer.music.load("sounds\\music\\theme.mp3")

def jump():
    num = randint(1, 5)
    jumps[num].play()

def play_music():
    mixer.music.play(-1)         # Joue indéfiniment
