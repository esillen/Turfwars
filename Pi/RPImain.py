import serverService
import sys
import robotControl
import serial

    



class Main():
    def __init__(self,port):
        self.robotControl = robotControl
        self.server = serverService.ServerService(PORT,self)
        self.server.start()
        
    def stop(self):
		robotControl.stop()

    #This method is called by the serverService.ServerService object
    #and determines what to do with a message.
    def receiveMessage(self, msg):
        if msg == 'exit':
            robotControl.terminate()
        elif msg=="stop":
            robotControl.stop()
        elif 'A'==msg[0] and 'B' in msg:
                #Messages are like 'A13B68' + (new line character) + perhaps more if something's wrong
                #TODO: Some more error handeling here perhaps?
                bpos = msg.find('B')
                robotControl.motorA.pwmControl(int(msg[1:bpos]))
                if 'A' in msg[bpos+1:]: #If there are more messages sent at a time
                    robotControl.motorB.pwmControl(int(msg[bpos+1:msg[bpos+1:].find('A')+bpos+1]))
                else:
                    robotControl.motorB.pwmControl(int(msg[bpos+1:]))
	
        





######  THE PROGRAM STARTS HERE ######
    
if (len(sys.argv)==1): #Argument variables
    PORT = 8888 # Arbitrary non-privileged port
else:
    PORT = int(sys.argv[1])

main = Main(PORT)

