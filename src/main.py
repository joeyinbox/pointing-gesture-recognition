#!/usr/bin/python
from PyQt5 import QtWidgets
from classes.DatasetGui import *


# Create a new Dataset GUI window and display it
app = QtWidgets.QApplication([])
gui = DatasetGui()
gui.show()

app.exec_()