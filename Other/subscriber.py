import socket,pickle,threading


class Subscriber(threading.Thread):

	def __init__(self,callback,host ='localhost',port = 50007):
		self.callback = callback
		self.host = host
		self.port = port
		self.keepGoing = True

	#What to do when data is received
	def data_callback(self,data):
		self.callback(data) #This is set somewhere else

	#Starts the socket and the thread
	def start_subscription(self):
		threading.Thread.__init__(self)

		HOST = self.host    # The remote host
		PORT = self.port             # The same port as used by the server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((HOST, PORT))

		self.start()

	def run(self):
		p = Protocol(self.callback)
		message = ''
		while self.keepGoing:
			data = self.sock.recv(1)
			if data == '#':
				p.process_data(message)
				message = ''
			else:
				message += data

	#Closes the connection and the thread
	def shutdown(self):
		self.keepGoing = False
		self.sock.close()



class Protocol:
	def __init__(self,callback):
		self.callback = callback

		self.at = None

		self.rows = None
		self.columns = None
		self.width = None
		self.height = None
		self.positions = []
		self.npositions = 0
		self.posCounter = 0
		self.grid = []
		self.crCounter = 0


	def data_callback(self,data):
		self.callback(data)

	def process_data(self,data):
		data = data.split(' ')

		if data[0] == 'wh':
			self.width = int(data[1])
			self.height = int(data[2])

		elif data[0] == 'cr':
			self.columns = int(data[1])
			self.rows = int(data[2])
			self.grid = []
			self.at = 'cr'

		elif data[0] == 'npos':
			self.npositions = data[1]
			self.at = 'npos'
			self.positions = []

		elif self.at == 'npos':
			if self.posCounter<self.npositions:
				self.positions.append([float(data[0]),float(data[1]),float(data[2])])
				self.posCounter += 1
			if self.posCounter == self.npositions:
				self.posCounter = 0
				self.at = None
				self.npositions = 0

		elif self.at=='cr':
			if self.crCounter<self.rows:
				rowData = []
				for element in data:
					rowData.append(int(element))
				self.grid.append(rowData)
				self.crCounter += 1
			if self.crCounter == self.rows:
				self.at = None
				self.data_callback([self.grid,self.positions,[self.width,self.height],[self.columns,self.rows]])
				self.crCounter = 0

