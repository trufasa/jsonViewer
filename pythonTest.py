import os
import sys
import json

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
        self.widget = self.ui.jsonTextEdit
        self.title = self.ui.titleLabel
        self.jsonViewArray = [self,]

    # loadPushButton command opens file dialog and fills table
    def loadJSON(self, widget):
        jsonFile = openFile([("JSON Files","*.json")])
        jsonFileName = os.path.basename(os.path.splitext(jsonFile)[0])
        self.setTitle(jsonFileName)

        if(jsonFile):
            with open (jsonFile) as jsonData:
                d = json.load(jsonData, object_pairs_hook = OrderedDict)

        filename = os.path.splitext(jsonFile)[0]
        filename = os.path.basename(filename)
        self.widget.setText(json.dumps(d, sort_keys=False, indent=2))

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

    def setTitle(self, title):
        self.title.setText(title)

    def appendCompareArray(self, newCompareObject):
        self.jsonViewArray.append(newCompareObject)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JSONView()
    window.ui.show()
    sys.exit(app.exec_())