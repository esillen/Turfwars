import socket
import sys
import time


class ServerService():

    def __init__(self,port,main):
        self.port = port
        self.main = main
        self.WRITE_DELAY = 0.05
        self.lastTime = time.time()
        
    def start(self):
        HOST = ''   # Symbolic name meaning all available interfaces
        wifisocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            wifisocket.bind((HOST, self.port))
        except socket.error:
            print( 'Bind failed, probably using an address already in use.' )
            sys.exit()
        print ('Socket bind complete')
        while True:
            wifisocket.listen(10)
            print( "ip: " + socket.gethostbyname(socket.gethostname()))
            #Here the connection to the client happens.
            conn, addr = wifisocket.accept()
            print ('Connected with ' + addr[0] + ':' + str(addr[1]))
            #Here's the loop that receives messages.
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        self.main.stop() #No more messages
                        break
                    if(data):
                    #The messages are sent to the main class which deals with them.
                        self.main.receiveMessage(data)
                        if(data=="exit"):
                            break           
            except KeyboardInterrupt:
                print( 'terminated by user')
                break
        conn.close()
        wifisocket.close()
        
        









 

 

    




