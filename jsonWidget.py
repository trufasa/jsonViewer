import os
import json

from collections import OrderedDict
from fileDialog import fileDialog
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class JSONWidget(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi("viewUI.ui", self)
        self.ui.loadPushButton.clicked.connect(self.loadJSON)
        self.widget = self.ui.jsonTextEdit
        self.title = self.ui.titleLabel
        self.jsonFileName = "Untitled"
        self.jsonDict = []

    def loadJSON(self):
        jsonFile = fileDialog([("JSON Files","*.json")])
        self.jsonFileName = os.path.basename(os.path.splitext(jsonFile)[0])

        if(jsonFile):
            with open (jsonFile) as jsonData:
                self.jsonDict = json.load(jsonData)#, object_pairs_hook = OrderedDict)

        self.widget.setText(json.dumps(self.jsonDict, sort_keys=False, indent=2))
        self.printName()

    def printName(self):
        print(self.jsonFileName)
        print(self.jsonDict)

    def compareJSON(self):
        self.jsonDict = difflib.Differ()
        result = d.compare(text1, text2)
        self.ui.json2TextEdit.setText('\n'.join(result))

    def setTitle(self, title):
        self.title.setText(title)