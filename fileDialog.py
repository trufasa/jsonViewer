import tkinter
from tkinter import filedialog

def fileDialog(fileTypes):
    fDialog = tkinter.Tk().withdraw()
    jsonFile = filedialog.askopenfilename(filetypes=fileTypes)
    return jsonFile