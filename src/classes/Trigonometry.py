#! /usr/bin/python
import sys, math



# Definition of the Trigonometry class
class Trigonometry:
	
	
	# Retrieve the intersection of the line of sight and the virtual sphere centered on the target
	# 
	# @param	eye					Coordinates of the master eye
	# @param	fingerTip			Coordinates of the fingertip
	# @param	target				Coordinates of the target
	# @param	radius				Radius of the virtual sphere
	# @return	array				Coordinates of the intersection
	def findIntersection(self, eye, fingerTip, target, radius):
		
		# Retrieve coordinates
		x1, y1, z1 = map(float, eye)
		x2, y2, z2 = map(float, fingerTip)
		x3, y3, z3 = map(float, target)
		r = radius
		
		
		# Line given as parametric equation:
		#x = x1 + (x2-x1)*t
		#y = y1 + (y2-y1)*t
		#z = z1 + (z2-z1)*t
		
		# Sphere equation:
		#(x-x3)**2 + (y-y3)**2 + (z-z3)**2 = r2
		
		# Substitute the line equation values of x,y,z into the sphere equation to get a quadratic equation for t: a*(t**2) + b*t + c = 0 where:
		a = (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
		b = 2*(((x2-x1)*(x1-x3)) + ((y2-y1)*(y1-y3)) + ((z2-z1)*(z1-z3)))
		c = x3**2 + y3**2 + z3**2 + x1**2 + y1**2 + z1**2 - 2*(x3*x1 + y3*y1 + z3*z1) - r**2
		
		# The solution for t is:
		#t = (-b(+-)math.sqrt(b**2 - 4*a*c))/(2*a)
		
		
		# Determine intersection
		dis = (b**2)-(4*a*c)
		
		if dis > 0:
			# The pointed direction passes through the sphere
			# The intersection points can be calculated by substituting t in the parametric line equations
			t1 = (-b + math.sqrt(dis))/(2*a)
			t2 = (-b - math.sqrt(dis))/(2*a)
			
			point1 = []
			point1.append(round(x1 + t1*(x2-x1)))
			point1.append(round(y1 + t1*(y2-y1)))
			point1.append(round(z1 + t1*(z2-z1)))
			
			point2 = []
			point2.append(round(x1 + t2*(x2-x1)))
			point2.append(round(y1 + t2*(y2-y1)))
			point2.append(round(z1 + t2*(z2-z1)))
			
			# Calculate the center point of the line from point1 to point2 to get the closest coordinates to the center of the target
			xd = (point1[0]+point2[0])/2
			yd = (point1[1]+point2[1])/2
			zd = (point1[2]+point2[2])/2
			
			return [xd, yd, zd]
			
		elif dis == 0:
			# The pointed direction is tangent to the sphere
			# The intersection point can be calculated by substituting t in the parametric line equations
			t1 = [-b/(2*a)]
			
			point = []
			point.append(round(x1 + t1*(x2-x1)))
			point.append(round(y1 + t1*(y2-y1)))
			point.append(round(z1 + t1*(z2-z1)))
			
			# The closest point is this only intersection
			return point
			
		else:
			return None
	
	
	# Retrieve the distance from the target and the intersection of the line of sight and the virtual sphere centered on the target
	# 
	# @param	eye					Coordinates of the master eye
	# @param	fingerTip			Coordinates of the fingertip
	# @param	target				Coordinates of the target
	# @param	radius				Radius of the virtual sphere
	# @return	float				Distance of the closest impact; otherwise None
	def findIntersectionDistance(self, eye, fingerTip, target, radius):
		# Retrieve target coordinates
		x3, y3, z3 = map(float, target)
		
		# Find eventual intersections
		intersection = self.findIntersection(eye, fingerTip, target, radius)
		
		if intersection != None:
			# Let's find the distance to the center of the target
			xd = x3-intersection[0]
			yd = y3-intersection[1]
			zd = z3-intersection[2]
			distance = math.sqrt(xd*xd + yd*yd + zd*zd)
			
			return distance
		else:
			return None
	
	
	# Returns the distance between two 3D points
	# 
	# @param	origin				Point A
	# @param	end					Point B
	# @return	float				Distance between the two points
	def get3dDistance(self, origin, end):
		x1, y1, z1 = map(float, origin)
		x2, y2, z2 = map(float, end)
		
		return math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)