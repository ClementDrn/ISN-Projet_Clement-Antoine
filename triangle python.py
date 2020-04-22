from tkinter import *
window=Tk()
canvas=Canvas (window,width=500,height=500)
canvas.create_polygon(10,10,10,60,50,35)
canvas.pack()

window.mainloop()