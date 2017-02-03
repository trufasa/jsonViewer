import os
import ast
import json
import difflib
from collections import OrderedDict
from fileDialog import openFile
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class JSONWidget(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi("viewUI.ui", self)
        self.ui.loadPushButton.clicked.connect(self.loadJSON)
        self.title = self.ui.titleLabel
        self.compareComboBox = self.ui.compareComboBox
        self.compareComboBox.currentIndexChanged.connect(self.compareJSON)
        self.currentJSON = ""
        self.parent = parent
        self.compareArray = [self.parent,]

    def loadJSON(self):
        jsonFile = openFile([("JSON Files","*.json")])
        jsonFileName = os.path.basename(os.path.splitext(jsonFile)[0])
        self.setTitle(jsonFileName)

        if(jsonFile):
            with open (jsonFile) as jsonData:
                jsonDict = json.load(jsonData)
        print(jsonDict)
        print(ast.literal_eval(jsonDict))
        self.fillWidget(json.loads(json.dump(ast.literal_eval(jsonDict))))

        for obj in self.compareArray:
            if(obj != self.parent):
                obj.resetCompareBox()

    # Fills single cell in table
    def fillItem(self, item, value):
        print(type(value))
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, key)
                item.addChild(child)
                item.setExpanded(True)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
                self.fillItem(child, val)
        elif type(value) is list:
            item.setText(1, str(value))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        else:
            item.setText(1, str(value))
            item.setExpanded(False)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    # Fills entire table widget
    def fillWidget(self, value):
        self.ui.treeWidget.clear()
        self.fillItem(self.ui.treeWidget.invisibleRootItem(), value)

    def compareJSON(self, compareObjIndex):
        diff = difflib.Differ()
        #result = list(diff.compare(self.currentJSON.splitlines(),
        #self.compareArray[compareObjIndex].currentJSON.splitlines()))
        #self.widget.setText('\n'.join(result))

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
        self.compareComboBox.addItem("Compare to...")
        for compareChild in self.compareArray:
            self.compareComboBox.addItem(compareChild.title.text())