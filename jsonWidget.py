import os
import json

from collections import OrderedDict
from fileDialog import openFile
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class JSONWidget(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi("viewUI.ui", self)
        self.ui.loadPushButton.clicked.connect(self.loadJSON)
        self.widget = self.ui.jsonTextEdit
        self.title = self.ui.titleLabel
        self.jsonDict = []
        self.compareComboBox = self.ui.compareComboBox
        self.parent = parent
        self.compareArray = []

    def loadJSON(self):
        jsonFile = openFile([("JSON Files","*.json")])
        jsonFileName = os.path.basename(os.path.splitext(jsonFile)[0])
        self.setTitle(jsonFileName)

        if(jsonFile):
            with open (jsonFile) as jsonData:
                self.jsonDict = json.load(jsonData)#, object_pairs_hook = OrderedDict)

        self.widget.setText(json.dumps(self.jsonDict, sort_keys=False, indent=2))

        for obj in self.compareArray:
            if(obj != self.parent):
                obj.resetCompareBox()

    def compareJSON(self):
        self.jsonDict = difflib.Differ()
        result = d.compare(text1, text2)
        self.ui.json2TextEdit.setText('\n'.join(result))

    def setTitle(self, title):
        self.title.setText(title)

    def appendCompareArray(self, newCompareObject):
        self.compareArray.append(newCompareObject)

    def popComboBox(self):
        self.compareComboBox.clear()
        for obj in self.compareArray:
            self.compareComboBox.addItem(obj.title.text())

    def resetCompareBox(self):
        self.compareComboBox.clear()
        for compareChild in self.compareArray:
            self.compareComboBox.addItem(compareChild.title.text())