#!/usr/bin/python
from PyQt5 import QtCore


# Hold a form item value and its associated methods
class FormItem(object):
	def __init__(self, value):
		self.value = ObservableVariable(value)
		self._initial_value = value


# Represent a value that can emit a "changed(new)" signal when the value is updated
class ObservableVariable(QtCore.QObject):
	# Register the signal
	changed = QtCore.pyqtSignal(object)
	
	def __init__(self, initial_value=0):
		super(ObservableVariable, self).__init__()
		self._value = initial_value
	
	# Getter of the value
	def get_value(self):
		return self._value
	
	# Setter of the value
	def set_value(self, new_val):
		try:
			self._value = int(new_val)
			self.changed.emit(new_val)
		except ValueError:
			pass
		
	
	# Apply getter and setter to the value
	value = property(get_value, set_value)
	
	def __str__(self):
		return str(self.value)
	
	# it can support more operators if needed
	def __iadd__(self, other):
		self.value += other
		return self
	
	def __isub__(self, other):
		self.value -= other
		return self