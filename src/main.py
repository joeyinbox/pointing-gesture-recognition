#!/usr/bin/python
from PyQt5 import QtWidgets
from classes.LiveGui import *


# Create a live GUI window and display it
app = QtWidgets.QApplication([])
gui = LiveGui()
gui.show()

app.exec_()