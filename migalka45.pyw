import tkinter
import time
from math import floor
from tkinter import *
from PIL import Image, ImageTk

def countdown(time):
    if time == -1:
        root.quit()
    root.after(500, countdown, time-1)

root = Tk()

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

root.attributes("-topmost", True)
root.geometry('%dx%d+%d+%d' % (sw, sh, 0, 0))

root.overrideredirect(1)
root.configure(bg='white')


image1 = Image.open("flower.png")
test = ImageTk.PhotoImage(image1)

label1 = tkinter.Label(image=test, borderwidth=0)
label1.image = test

# Position image
label1.place(x=sw/2-50, y=sh/2-50)

countdown(0)

root.mainloop()
