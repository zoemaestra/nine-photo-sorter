import tkinter as tk
from tkinter import ttk
from PIL import Image,  ImageTk
from os import listdir, remove, mkdir
from os.path import isfile, join, isdir
import shutil
import threading
if isdir("DELETE") == False:
    mkdir("DELETE")
files = [f for f in listdir(".//") if isfile(join(".//", f))]
images = []
currentImage = 0
allowedExtensions = ["png",
                     "jpg",
                     "jpeg",
                     "gif",
                     "bmp"]
allowedKeys = {"1":"Memes",
               "2":"Kitties",
               "3":"Other",
               "4":"Trash",
               "5":"Trash Lite",
               "6":"Selfies",
               "7":"Cute",
               "8":"Cool",
               "9":"Lewds",
               "0":"Art",
               "minus":"Justin",
               "equal":"Useful",
               "Delete":"DELETE"}

for file in files:
    if file.split(".")[-1].lower() in allowedExtensions:
        images.append(file)

win = tk.Tk()
win.geometry("500x840")

def move(src,dest):
    shutil.move(src,dest)

def keydown(e):
    global currentImage
    if currentImage >= len(images):
        image_label.config(image='',text="No more images!",font=("Arial", 30))
    else:
        if e.keysym in allowedKeys:
            shutil.move(f".\{images[currentImage]}",f".\{allowedKeys[e.keysym]}\{images[currentImage]}")
            currentImage += 1
            if currentImage < len(images):
                img2 = resizeImage(images[currentImage])
                imagefilename.configure(text=images[currentImage])
                imagefilename.text = images[currentImage]
                image_label.configure(image=img2)
                image_label.image = img2

def resizeImage(imageFileName):
    basewidth = 500
    baseheight = 500
    img = Image.open(imageFileName)
    wpercent = (basewidth/float(img.size[0]))
    hpercent = (baseheight/float(img.size[1]))

    hsize = int((float(img.size[1])*float(wpercent)))
    wsize = int((float(img.size[0])*float(hpercent)))

    while img.size[0] > basewidth or img.size[1] > baseheight:
        if img.size[0] > basewidth:
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            basewidth = img.size[0]
        if img.size[1] > baseheight:
            img = img.resize((wsize,baseheight), Image.ANTIALIAS)
            baseheight = img.size[1]
        hsize = int((float(img.size[1])*float(wpercent)))
        wsize = int((float(img.size[0])*float(hpercent)))
    img =  ImageTk.PhotoImage(img)
    return img

image_label = ttk.Label(win)
if len(images) > 0:
    imagefilename = ttk.Label(win,text=images[currentImage],font=("Arial", 20))
    img2 = resizeImage(images[currentImage])
    image_label.configure(image=img2)
    image_label.image = img2
else:
    imagefilename = ttk.Label(win,text="No images!",font=("Arial", 20))
    image_label.config(image='',text="Place the .exe in photo folder!",font=("Arial", 25))
    
imagefilename.pack()
image_label.pack()
info = ttk.Label(win,text="""
Press the following keyboard keys to move to the
corresponding folder:
1: Memes
2: Kitties
3: Other
4: Trash
5: Trash Lite
6: Selfies
7: Cute
8: Cool
9: Lewds
0: Art
-: Justin
=: Useful

Del: Delete
""",font=("Arial", 11))
info.place(x=0,y=540)

win.bind("<Key>", keydown)
win.mainloop()
