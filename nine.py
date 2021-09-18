import tkinter as tk
from tkinter import ttk
from PIL import Image,  ImageTk
from os import listdir, remove, mkdir,rename
from os.path import isfile, join, isdir
import shutil
import threading
import re

files = [f for f in listdir(".//") if isfile(join(".//", f))]
images = []
currentImage = 0
allowedExtensions = ["png",
                     "jpg",
                     "jpeg",
                     "gif",
                     "bmp"]

for file in files:
    if file.split(".")[-1].lower() in allowedExtensions:
        images.append(file)

win = tk.Tk()
win.geometry("500x640")

def keydown(e):
    global currentImage
    if currentImage >= len(images)-1:
        image_label.config(image='',text="No more images!",font=("Arial", 30))
        imagefilename.configure(text="")
        newImageName.configure(state="disabled")
    else:
        imageFileExt = images[currentImage].split(".")[-1:]
        safeNewImageName = newImageName.get().replace("<","").replace(">","").replace("?","").replace(":","").replace("*","").replace("|","").replace("/","").replace("\\","").replace("\"","")
        rename(images[currentImage], safeNewImageName+"."+imageFileExt[0])

        currentImage += 1
        if currentImage < len(images):
            imagefilename.configure(text=images[currentImage])
            imagefilename.text = images[currentImage]
            try:
                img2 = resizeImage(images[currentImage])
                image_label.configure(image=img2)
                image_label.image = img2

                imageFileNameNoExt = ""
                if len(images[currentImage].split(".")[:-1]) > 1:
                    for word in images[currentImage].split(".")[:-1]:
                        imageFileNameNoExt = imageFileNameNoExt + word + "."
                    imageFileNameNoExt = imageFileNameNoExt[:-1]
                else:
                    imageFileNameNoExt = images[currentImage].split(".")[:-1][0]

                newImageName.delete(0,'end')
                newImageName.insert(0,imageFileNameNoExt)

            except Exception as e:
                image_label.config(image='',text="Error displaying image",font=("Arial", 25))
                print(e)
    newImageName.focus()


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
imageFileNameNoExt = ""
if len(images) > 0:
    imagefilename = ttk.Label(win,text=images[currentImage],font=("Arial", 20))
    try:
        img2 = resizeImage(images[currentImage])
        image_label.configure(image=img2)
        image_label.image = img2


        if len(images[currentImage].split(".")[:-1]) > 1:
            for word in images[currentImage].split(".")[:-1]:
                imageFileNameNoExt = imageFileNameNoExt + word + "."
            imageFileNameNoExt = imageFileNameNoExt[:-1]
        else:
            imageFileNameNoExt = images[currentImage].split(".")[:-1][0]
    except Exception as e:
        image_label.config(image='',text="Error displaying image",font=("Arial", 25))
        print(e)

else:
    imagefilename = ttk.Label(win,text="No images!",font=("Arial", 20))
    image_label.config(image='',text="Place the .exe in photo folder!",font=("Arial", 25))

imagefilename.pack()
image_label.pack()
info = ttk.Label(win,text="""Enter filename and press enter to save (excluding extensions)
A file name can't contain any of the following characters:
\ / : * ? " < > |""",font=("Arial", 11)).pack()
newImageName = ttk.Entry(width=70,font=("Arial", 16))
newImageName.pack()
newImageName.focus()
newImageName.insert(0,imageFileNameNoExt)

win.bind("<Return>", keydown)
win.mainloop()
