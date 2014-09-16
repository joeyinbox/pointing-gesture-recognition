#! /usr/bin/python
import hashlib, time


class Testing:
	
	enabled = False
	timer = 0
	timerTotal = 0
	sampleSize = 100
	data = {"stop":{"total":0,"count":0}}
	
	def isEnabled(self):
		return self.enabled
		
	def startTimer(self):
		if self.enabled:
			self.timer = time.time()
			self.timerTotal = 0
	
	def timerMarker(self, title):
		if self.enabled:
			timeElapsed = (time.time()-self.timer)*1000
			hash = hashlib.md5(title).hexdigest()
			
			if hash in self.data:
				self.data[hash]["count"] += 1
				self.data[hash]["total"] += timeElapsed
			else:
				self.data[hash] = {"count":1,"total":timeElapsed,"title":str(title)}
			
			#print("--- {0:0.6f} ms \t--- Average: {1:0.6f} ms \t{2}".format(timeElapsed, (self.data[hash]["total"]/self.data[hash]["count"]), str(title)))
			
			self.timer = time.time()
			self.timerTotal += timeElapsed
	
	def stopTimer(self):
		if self.enabled:
			self.timerTotal += (time.time()-self.timer)*1000
			
			self.data["stop"]["count"] += 1
			self.data["stop"]["total"] += self.timerTotal
			
			# Prints the results every X frames
			if self.data["stop"]["count"] >= self.sampleSize:
				print("------------------------\n--- Average execution time over {0} frames\n------------------------".format(self.sampleSize))
				for i in self.data.keys():
					if i != "stop":
						print("--- {0:0.6f} ms \t{1}".format((self.data[i]["total"]/self.data[i]["count"]), self.data[i]["title"]))
				print("------------------------\n--- Total: {0:0.6f} ms\n------------------------".format((self.data["stop"]["total"]/self.data["stop"]["count"])))
						
				
				# Reinitialise the data
				self.data = {"stop":{"total":0,"count":0}}
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				