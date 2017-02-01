import tkinter
from tkinter import filedialog

def openFile(fileTypes):
    fDialog = tkinter.Tk().withdraw()
    jsonFile = filedialog.askopenfilename(filetypes=fileTypes)
    return jsonFile