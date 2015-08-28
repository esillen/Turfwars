##########################
#### DON'T TOUCH!!!!! ####
##########################

import subscriber,sys,signal,math,robotClient

grid = []
positions = []
fieldWidth = 0
fieldHeight = 0
columns = 0
rows = 0

sub = None

def signal_handler(signal, frame):
	sub.shutdown()
	sys.exit(0)

def data_received(data):
	global grid,positions,fieldWidth,fieldHeight,columns,rows
	
	grid = data[0]
	positions = data[1]
	fieldWidth = data[2][0]
	fieldHeight = data[2][1]
	columns = data[3][0]
	rows = data[3][1]


def start_subscription(ip):

	#sub's callback method is the first argument.
	sub = subscriber.Subscriber(data_received,ip,50007)
	#To shut down properly
	signal.signal(signal.SIGINT, signal_handler)
	sub.start_subscription()

    
######################
####  TOUCH!!!!!  ####
######################

#Variables
rpiIP = "192.168.1.241" #Ip of your Pi
judgeIP = "localhost" 	#Ip of the judge
myId = 0 #Your id. Will be given to you before each game.

#Called from robotClient.py and this is how you control your robot
def robot_control():
	
	
	if positions: #this is to make sure that we got any data at all.
		percentA,percentB = super_duper_algorithm()
		
	else:
	
		#test your robot here
		percentA = 20
		percentB = 20
	
		
	return [percentA,percentB]


#replace by smart algorithm
def super_duper_algorithm():
	botx,boty,angle = positions[myId]
	#this is how the program calculates your position in the grid
	gridx = int(math.floor((botx/fieldWidth)*columns)) 
	gridy = int(math.floor((boty/fieldHeight)*rows))

	#radAngle = math.radians(angle)
	print botx,boty,gridx,gridy,angle
	#print grid
	
	return 0,0


###################
### THE PROGRAM ###
###################

#uncomment if you want to connect to the judge
#start_subscription(judgeIP) 

#Uncomment if you want to connect to your Pi
robotClient.start_client(rpiIP,robot_control)


