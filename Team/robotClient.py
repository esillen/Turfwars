# -*- coding: cp1252 -*-
import socket   #for sockets
import sys  #for exit
import time

def start_client(ip,controlCallback):
	try:
		#create an AF_INET, STREAM socket (TCP)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
		sys.exit();
	 
	print 'Socket Created'

	#change to appropriate host
	host = ip
	port = 8888
	 
	#Connect to remote server
	s.connect((host , port))
	s.setblocking(0) #non-blocking communication
	print 'Socket Connected to ' + host


	#Send some data to remote server
	while True:
		#message = raw_input("meddelande till servern: ")
		message = "start"
		try :
		    #Send the message
		    s.sendall(message)
		except socket.error:
		    #Send failed
		    print 'Send failed'
		    sys.exit()
		if message=="exit": #Write exit to exit the application. The server shuts down properly if "exit" is sent.
		    break
		elif message =="start":
			try:
				print "sending pwm requests..."
				while 1:
				    stuff = controlCallback()
				    #Test the participants outputs
				    try:
				    	aPWM = max(min(int(stuff[0]),100),-100)
				    	bPWM = max(min(int(stuff[1]),100),-100)
				    except:
				        print('Something is wrong in your outputs, they look like this: ')
				        print(stuff[0],stuff[1])
				        aPWM = 0
				        bPWM = 0
				    message = 'A'+str(aPWM)+'B'+str(bPWM)
				    s.sendall(message) #Send data like "A50B100"
				    time.sleep(0.1)
				
			except KeyboardInterrupt: #You can cancel by pressing ctrl+c
				print "stopped sending pwm requests!"
				break
	 

	 
	print 'Messages send successfully'
