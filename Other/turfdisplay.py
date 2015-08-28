import subscriber,pygame,math
 
class TurfDisplay:
    def __init__(self,ip = "localhost"):
        self.windowHeight = 600
        self.windowWidth = 800
        pygame.init()
        self.surface = pygame.display.set_mode((self.windowWidth,self.windowHeight))
        col0 = (255,255,255)
        col1 = (188,55,133)
        col2 = (18,108,161)
        col3 = (0,0,255)
        col4 = (0,0,0)
        colors = (col0,col1,col2,col3,col4)
        self.colors = []
        for col in colors:
            self.colors.append(pygame.Color(col[0],col[1],col[2]))
        self.judgeIp = ip
 
        self.grid = []
        self.positions = []
        self.fieldWidth = 0
        self.fieldHeight = 0
        self.columns = 0
        self.rows = 0
        self.sub = subscriber.Subscriber(self.data_callback,self.judgeIp)
        self.sub.start_subscription()

    def data_callback(self,data):
        self.grid = data[0]
        self.positions = data[1]
        self.fieldWidth = data[2][0]
        self.fieldHeight = data[2][1]
        self.columns = data[3][0]
        self.rows = data[3][1]
        self.update_interface()
 
    def update_interface(self):
        self.surface.fill((255,255,0))
        rectWidth = (self.windowWidth/self.rows)
        rectHeight = (self.windowHeight/self.columns)
        for row in range(self.rows):
            for column in range(self.columns):
                pygame.draw.rect(self.surface,self.colors[self.grid[column][row]],(column*rectWidth,row*rectHeight,rectWidth,rectHeight))
        
        for index,position in enumerate(self.positions):
            x = int((position[0]/self.fieldWidth)*self.windowWidth)
            y = int((position[1]/self.fieldHeight)*self.windowHeight)
            pygame.draw.circle(self.surface,pygame.Color(0,0,0),(x,y),15, 4)
            pygame.draw.circle(self.surface,self.colors[index+1],(x,y),11)
            angle = position[2]
            x2 = x+math.cos(math.radians(angle))*30
            y2 = y-math.sin(math.radians(angle))*30 #Because of the flipped coordinate system...
            pygame.draw.line(self.surface,pygame.Color(0,0,0),(x,y),(x2,y2),3)
        pygame.display.update()
 
host = "192.168.1.217"
td = TurfDisplay()
