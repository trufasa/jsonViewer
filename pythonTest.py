import os
import sys
import json

from jsonWidget import JSONWidget
from collections import OrderedDict
from fileDialog import fileDialog
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class JSONView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.ui = uic.loadUi("testUI.ui")

        self.ui.loadPushButton.clicked.connect(self.loadJSON)
        self.ui.addPushButton.clicked.connect(self.addWidget)
        self.widget = self.ui.jsonTextEdit
        self.jsonViewArray = []

    # loadPushButton command opens file dialog and fills table
    def loadJSON(self, widget):
        jsonFile = fileDialog([("JSON Files","*.json")])

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JSONView()
    window.ui.show()
    print(window.jsonViewArray)
    sys.exit(app.exec_())