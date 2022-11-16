# ==== IMPORTS =============================================================== #

import math
import time

# ==== CLASSES =============================================================== #

class City():
	
	def __init__(self, residents):
		"""
		residents := ([[str]]) a nested list representing each resident's travel
		"""
		
		self.locations = list(set([i for l in residents for i in l]))
		self.traversal = {location:{} for location in self.locations}
		self.map       = Map(len(self.locations))
		
		for places in residents:
			
			for index in range(len(places) - 1):
				
				if places[index + 1] not in self.traversal[places[index]]:
					self.traversal[places[index]][places[index + 1]] = 1
				else:
					self.traversal[places[index]][places[index + 1]] += 1
	
	
	def optimize_0(self):
		# Commonly use edge method ?
		pass
	
	
	def optimize_1(self):
		# Most interconnected vertices method ?
		pass


class Map():
	
	def __init__(self, size):
		"""
		size := (uint) the size of the map for x and y - [-size, size]
		"""
		
		self.plane = {x:{y:None for y in range(-size, size + 1)} for x in range(-size, size + 1)}
		self.point = [Pair(0, 0)]
	
	
	def access(self, x, y):
		
		return self.plane[x][y]
	
	
	def border(self):
		
		return self.point
	
	
	def insert(self, x, y, name):
		
		if Pair(x, y) in self.point:
			
			self.plane[x][y] = name
			
			self.point.remove(Pair(x, y))
			
			if self.plane[x + 1][y] is None: self.point.append(Pair(x + 1, y))
			if self.plane[x - 1][y] is None: self.point.append(Pair(x - 1, y))
			if self.plane[x][y + 1] is None: self.point.append(Pair(x, y + 1))
			if self.plane[x][y - 1] is None: self.point.append(Pair(x, y - 1))
		
		else:
			
			print("ERROR: (%d, %d) is not a coordinate on the border..." %(x, y))


class Pair():
	
	def __init__(self, x, y):
		
		self.x = x
		self.y = y
	
	
	def __eq__(self, X):
		
		return self.x == X.x and self.y == X.y
	
	
	def dist(self, X):
		
		return abs(X.x - self.x) + abs(X.y - self.y)


# ==== EOF =================================================================== #

a = ["Home A", "Gym", "Library", "Home A"]
b = ["Home B", "School", "Store", "Theatre", "Car Dealer", "Home B"]
c = ["Apartment", "School", "Gym", "Home A", "Work", "Apartment"]

X = City([a, b, c])

#print(X.locations)
#print(X.traversal)
#print(X.map.plane)

Y = Map(5)

Y.insert(0, 0, "Gym")
Y.insert(2, 3, "House")

for i in Y.point:
	
	print(i.x, i.y)
