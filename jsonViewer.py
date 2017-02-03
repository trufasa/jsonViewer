import os
import sys
import json
import ast
from jsonWidget import JSONWidget
from collections import OrderedDict
from fileDialog import openFile
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class JSONView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.ui = uic.loadUi("testUI.ui")

        self.ui.loadPushButton.clicked.connect(self.loadJSON)
        self.ui.addPushButton.clicked.connect(self.addWidget)
        self.ui.savePushButton.clicked.connect(self.saveJson)
        
        self.widget = self.ui.treeWidget
        self.title = self.ui.titleLabel
        self.jsonViewArray = [self,]
        self.currentJSON = ""
        self.childrenArray = dict()
        self.revertDict = []
        self.parentsArray = []

    # loadPushButton command opens file dialog and fills table
    def loadJSON(self, widget):
        jsonFile = openFile([("JSON Files","*.json")])
        jsonFileName = os.path.basename(os.path.splitext(jsonFile)[0])
        self.setTitle(jsonFileName)

        if(jsonFile):
            with open (jsonFile) as jsonData:
                jsonDict = json.load(jsonData, object_pairs_hook = OrderedDict)
        
        self.fillWidget(json.loads(json.dumps(jsonDict)))
        #self.currentJSON = json.dumps(jsonDict, sort_keys=False, indent=2)
        #self.widget.setText(self.currentJSON)
        
        for obj in self.jsonViewArray:
            if(obj != self):
                obj.resetCompareBox()

    def addWidget(self):
        widget = JSONWidget(self)
        self.ui.textHorizontalLayout.addWidget(widget.ui)
        self.jsonViewArray.append(widget)
        widget.setTitle("Untitled %d" % len(self.jsonViewArray))
        for obj in self.jsonViewArray:
            if(obj != widget):
                widget.appendCompareArray(obj)
                widget.resetCompareBox()
                if(obj != widget.parent):
                    obj.appendCompareArray(widget)
                    obj.resetCompareBox()
        widget.popComboBox()

    # Fills single cell in table
    def fillItem(self, item, value):
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

    def setTitle(self, title):
        self.title.setText(title)

    def appendCompareArray(self, newCompareObject):
        self.jsonViewArray.append(newCompareObject)

    def children(self, parent):
        childCount = parent.childCount()
        #print(parent.text(0))
        #print(parent.parent())
        if childCount > 0:
            if parent.parent():
                dictArray = []
                self.childrenArray = []
                for index in range(childCount):
                    self.children(parent.child(index))
                iterChildren = iter(self.childrenArray)
                iterArray = dict(zip(iterChildren, iterChildren))
                self.childrenArray = []
                self.childrenArray.append(iterArray)
                self.childrenArray = []
                self.childrenArray.append(parent.text(0))
                self.childrenArray.append(iterArray)
                print(self.childrenArray)
            else:
                self.parentsArray.append(parent)
                for index in range(childCount):
                    self.children(parent.child(index))
        elif parent.text(1):
            value0 = parent.text(0)
            value1 = parent.text(1)
            self.childrenArray.append(value0)
            self.childrenArray.append(value1)

    def saveJson(self):
        # Getting children
        dictArray = dict()

        for index in range(self.ui.treeWidget.topLevelItemCount()):
            self.childrenArray = []
            parent = self.ui.treeWidget.topLevelItem(index)
            self.children(parent) 
            iterChildren = iter(self.childrenArray)
            childDict = dict(zip(iterChildren, iterChildren))
            dictArray[parent.text(0)] = childDict

        with open('test.json', 'w') as outfile:
            json.dump(dictArray, outfile, indent = 2)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JSONView()
    window.ui.show()
    sys.exit(app.exec_())