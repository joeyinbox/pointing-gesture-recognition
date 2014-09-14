#! /usr/bin/python
import time


class Testing:
	
	enabled = False
	timer = 0
	timerTotal = 0
		
	def startTimer(self):
		if self.enabled:
			self.timer = time.time()
			self.timerTotal = 0
	
	def timerMarker(self, title):
		if self.enabled:
			timeElapsed = (time.time()-self.timer)*1000
			print("--- {0:0.6f} ms \t{1}".format(timeElapsed, str(title)))
			
			self.timer = time.time()
			self.timerTotal += timeElapsed
	
	def stopTimer(self):
		if self.enabled:
			self.timerTotal += (time.time()-self.timer)*1000
			print("------------------------\n--- Execution time: {0:0.6f} ms\n------------------------".format(self.timerTotal))
		
	def isEnabled(self):
		return self.enabled