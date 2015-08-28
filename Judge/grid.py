

#Pygame to be able to plot the grid
#New positions of robots happens here in "update"
import pygame,sys,math,random


pygame.init()

windowSurface = pygame.display.set_mode((800,600))
col0 = (255,255,255)
col1 = (255,0,0)
col2 = (0,255,0)
col3 = (0,0,255)
col4 = (0,0,0)
defaultColors = (col1,col2,col3,col4)


class Grid():
	def __init__(self,fw,fh, cols = 40, rows = 40,colors = defaultColors):
		self.colors = [pygame.Color(255,255,255)]
		for col in colors:
			self.colors.append(pygame.Color(col[0],col[1],col[2]))

		self.surface = windowSurface
		self.fieldWidth = float(fw)
		self.fieldHeight = float(fh)
		self.columns = float(cols)
		self.rows = float(rows)
		#initiate field
		self.robotPositions = []
		self.mainArray = []
		for i in range(int(self.rows)):#ys
			row = []
			for j in range(int(self.columns)): #xes
				row.append(0)
			self.mainArray.append(row)



	#Updates the grid with new positions of the robots
	def update(self,positions):
		self.robotPositions = positions
		indexes = range(len(positions))
		random.shuffle(indexes)#randomize who goes first
		for i in indexes: 
			pos = positions[i]
			if pos:
				x = pos[0]
				y = pos[1]
				angle = pos[2]
				arrayx = int(math.floor((x/self.fieldWidth)*self.columns))
				arrayy = int(math.floor((y/self.fieldHeight)*self.rows))
				neighborhood = self.get_neighborhood(arrayx,arrayy,depth = 2)
				for neighbor in neighborhood:
					self.mainArray[neighbor[0]][neighbor[1]] = i+1 #1-indexed. 0 means not yet taken.
				
				
				
				
	#This will color around a postion to a certain depth
	#Does a breadth-first search
	def get_neighborhood(self,x,y,depth = 1):
		neighbors = [(x,y)]
		if depth==1:
			return neighbors
		for i in range(depth):
			for neighbor in neighbors[:]:
				x = neighbor[0]
				y = neighbor[1]
				up = (x,y+1)
				down = (x,y-1)
				left = (x-1,y)
				right = (x+1,y)
				for direction in up,down,left,right:
					x = direction[0]
					y = direction[1]
					if direction not in neighbors and x>=0 and y>=0 and x<int(self.rows) and y < int(self.columns):
						neighbors.append(direction)
		return neighbors
		

	#draws the grid using pygame surface. A little ugly.
	def draw_grid(self):
		rectWidth = int(float(self.fieldWidth)/float(self.columns))
		rectHeight = int(float(self.fieldHeight)/float(self.rows))
		for y in range(int(self.rows)):
			for x in range(int(self.columns)):
				pos = (int(float(x)*float(self.fieldWidth)/float(self.columns)),int(float(y)*float(self.fieldHeight)/float(self.rows)))
				pygame.draw.rect(windowSurface,self.colors[self.mainArray[y][x]],(pos[0],pos[1],rectWidth,rectHeight))
		pygame.display.update()

	#returns the current grid and the robot posistions
	def get_data(self):
		return self.mainArray,self.robotPositions
