import os
import sys
import json
import tkinter
from tkinter import filedialog
from pprint import pprint
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets, QtGui


class JSONView(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)

		self.ui = uic.loadUi("testUI.ui")
		self.treeWidget = self.ui.jsonTreeWidget

		self.ui.loadPushButton.clicked.connect(self.loadJSON)


	def loadJSON(self):
		fDialog = tkinter.Tk()
		jsonFile = filedialog.askopenfilename()
		fDialog.destroy()

		with open (jsonFile) as jsonData:
			d = json.load(jsonData)

		path, filename = os.path.split(jsonFile)

		self.fillWidget(d, filename)

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

	def fillWidget(self, value, title):
		self.treeWidget.clear()
		self.treeWidget.setHeaderLabel(title)
		self.fillItem(self.treeWidget.invisibleRootItem(), value)



app = QtWidgets.QApplication(sys.argv)
windowUI = JSONView()
windowUI.ui.show()
app.exec_()
