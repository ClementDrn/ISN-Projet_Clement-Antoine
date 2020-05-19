from threading import Thread
import time


def a():
    thread1 = Thread(target=b)
    thread1.start()

def b():
    global c
    time.sleep(1)
    print(c)
    c += 1

c = 1
a()
a()
a()
a()
a()
a()
a()
a()
a()
a()
