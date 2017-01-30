import os
import sys
import json
import tkinter
import difflib

from collections import OrderedDict
from functools import partial
from tkinter import filedialog
from pprint import pprint
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets, QtGui


class JSONWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = uic.loadUi("viewUI.ui")
        self.ui.loadPushButton.clicked.connect(self.loadJSON)

    def loadJSON(self):
        fDialog = tkinter.Tk().withdraw()
        jsonFile = filedialog.askopenfilename(filetypes=[("JSON Files","*.json")])

        if(jsonFile):
            with open (jsonFile) as jsonData:
                d = json.load(jsonData, object_pairs_hook = OrderedDict)

        self.widget.setText(json.dumps(d, sort_keys=False, indent=2))

class JSONView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.ui = uic.loadUi("testUI.ui")
        #self.ui.json2TreeWidget.clear()
        self.ui.load1PushButton.clicked.connect(partial(self.loadJSON, self.ui.json1TextEdit))
       # self.ui.load2PushButton.clicked.connect(partial(self.loadJSON, self.ui.json2TextEdit))
        self.ui.comparePushButton.clicked.connect(self.compareJSON)
        self.ui.addPushButton.clicked.connect(self.addWidget)

    # loadPushButton command opens file dialog and fills table
    def loadJSON(self, widget):
        fDialog = tkinter.Tk().withdraw()
        jsonFile = filedialog.askopenfilename(filetypes=[("JSON Files","*.json")])
        #check = widget.columnCount()
        #print(check)
        if(jsonFile):
            with open (jsonFile) as jsonData:
                d = json.load(jsonData, object_pairs_hook = OrderedDict)
        print(d)
        filename = os.path.splitext(jsonFile)[0]
        filename = os.path.basename(filename)
        widget.setText(json.dumps(d, sort_keys=False, indent=2))


    def compareJSON(self, value):
        text1 = self.ui.json1TextEdit.toPlainText().splitlines()
        text2 = self.ui.json2TextEdit.toPlainText().splitlines()
        d = difflib.Differ()
        result = d.compare(text1, text2)
        self.ui.json2TextEdit.setText('\n'.join(result))

    def addWidget(self):
        widget = JSONWidget().ui
        self.ui.textHorizontalLayout.addWidget(widget)


app = QtWidgets.QApplication(sys.argv)
windowUI = JSONView()
windowUI.ui.show()
app.exec_()