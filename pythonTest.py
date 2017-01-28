import os
import sys
import json
import tkinter
from functools import partial
from tkinter import filedialog
from pprint import pprint
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets, QtGui

class JSONView(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = uic.loadUi("testUI.ui")
        self.ui.json1TreeWidget.clear()
        self.ui.json2TreeWidget.clear()
        self.ui.load1PushButton.clicked.connect(partial(self.loadJSON, self.ui.json1TreeWidget))
        self.ui.load2PushButton.clicked.connect(partial(self.loadJSON, self.ui.json2TreeWidget))

    # loadPushButton command opens file dialog and fills table
    def loadJSON(self, widget):
        fDialog = tkinter.Tk().withdraw()
        jsonFile = filedialog.askopenfilename(filetypes=[("JSON Files","*.json")])
        check = widget.columnCount()
        print(check)
        if(jsonFile):
            with open (jsonFile) as jsonData:
                d = json.load(jsonData)

        filename = os.path.splitext(jsonFile)[0]
        filename = os.path.basename(filename)
        self.fillWidget(d, filename, widget)

        self._replaceJson(widget)


    # Fills single cell in table
    def fillItem(self, item, value):
        item.setExpanded(True)
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, key)
                item.addChild(child)
                item.setExpanded(False)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
                self.fillItem(child, val)
        elif type(value) is list:
            for val in value:
                child = QTreeWidgetItem()
                item.addChild(child)
                if type(val) is dict:
                    child.setText(0, '[dict]')
                elif type(val) is list:
                    child.setText(0, '[list]')
                else:
                    child.setText(0, unicode(val))
                child.setExpanded(False)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
        else:
            child = QtWidgets.QTreeWidgetItem()
            child.setText(0, value)
            child.setExpanded(False)
            child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
            item.addChild(child)

    # Fills entire table widget
    def fillWidget(self, value, title, widget):
        widget.clear()
        widget.setHeaderLabel(title)
        self.fillItem(widget.invisibleRootItem(), value)

    def compareJSON(dict1, dict2):
        for x, y in zip(x.iteritems(), y.iteritems()):
            if x != y:
                print("Not", x, y)

    def children(self, parent):
        global children
        childCount = parent.childCount()
        if childCount:
            for index in range(childCount):
                self.children(parent.child(index))
        elif not parent.parent() and not parent.text(0):  # top levels without children
            children.append(parent)
        if parent.text(0):
            children.append(parent)

    def generateString(self, treeItem):
        def getParent(item):
            if item.parent():
                global parents
                parents.append(str(item.parent().text(0)))
                getParent(item.parent())
        global parents
        parents = [str(treeItem.text(0))]
        getParent(treeItem)
        attribute, value = '.'.join(parents[::-1]), treeItem.text(1)
        return attribute, value

    def _replaceJson(self, widget):
        # Getting children
        global children
        children = []
        for index in range(widget.topLevelItemCount()):
            parent = widget.topLevelItem(index)
            self.children(parent)
        # Generating config string
        for child in children:
            attribute, value = self.generateString(child)
            print(attribute)


app = QtWidgets.QApplication(sys.argv)
windowUI = JSONView()
windowUI.ui.show()
app.exec_()