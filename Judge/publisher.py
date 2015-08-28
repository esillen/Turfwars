import socket,threading

class Client():
	def __init__(self,connection,id):
		self.connection = connection
		self.id = id
		self.alive = True


	def sendall(self,data):
		if self.alive:
			try:
				self.connection.sendall(data)
			except:
				self.connection.close()
				self.alive = False

	def close(self):
		try:
			self.connection.close()
		except:
			pass #not much to do, socket already closed.

class Publisher(threading.Thread):
	def __init__(self,port = 50007):
		threading.Thread.__init__(self)
		self.port = port
		self.keepGoing = True
		self.clients = []

	def run(self):
		HOST = ''
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print("open on port " + str(self.port))
		s.bind((HOST, self.port))
		s.listen(4)
		index = 0
		while self.keepGoing:
			conn, addr = s.accept()
			print 'Connected by', addr
			self.clients.append(Client(conn,index))
			index+=1

	#Publishes the data.
	#Warning! You need to read the entire data on the other side to read properly!
	def publish(self,grid,positions,widthHeight,columnsRows):
		for client in self.clients:
			client.sendall('wh '+str(widthHeight[0])+' '+str(widthHeight[1]) + '#')
			client.sendall('npos ' + str(len(positions)) + '#')
			for pos in positions:
				if pos:
					client.sendall(str(pos[0]) + ' ' + str(pos[1]) + ' ' +str(pos[2])+ '#')
				else:
					client.sendall("0.0 0.0 0.0#")
			client.sendall("cr "+str(columnsRows[0])+' '+str(columnsRows[1])+ '#')
			for row in grid:
				rowString = ''
				for element in row:
					rowString+=str(element) #I know this is dumb...
				client.sendall(' '.join(rowString)+ '#')

	#Closes the thread and the connection
	def shutdown(self):
		self.keepGoing = False
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('localhost', self.port))
		for client in self.clients:
			client.close()
		s.close()









