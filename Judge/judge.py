import ceilingCam,publisher
import grid,time
import signal,sys


pub = None

def signal_handler(signal, frame):
	print('Closing connection')
	pub.shutdown()

	#s.close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def main():
	global pub
	numberOfRobots = 2
	rows = 40
	columns = 40
	sendDelay = 1.0
	lastTime = time.time()
	

	'''
	while True:
		try:
			numberOfRobots = int(raw_input("number of robots: "))
			break
		except:
			print("wrong input, try again")

	'''
	
	print '''
	##########

	CALIBRATION STARTING

	##########
	'''
	playField,positionColor,teamColors = ceilingCam.calibrate_everything(int(numberOfRobots))
	mainGrid = grid.Grid(playField[2],playField[3],cols = columns,rows = rows,colors = teamColors)
	pub = publisher.Publisher(50007)
	pub.start()



	##THE ACTUAL GAME LOOP
	while True:
		posret = ceilingCam.detectRobots(playField,positionColor,teamColors)
		if not posret:
			continue
		
		mainGrid.update(posret)
		#mainGrid.draw_grid()

		if time.time()-lastTime>sendDelay:
			gridData,positionData = mainGrid.get_data()
			pub.publish(gridData,positionData,(playField[2],playField[3]),(columns,rows))#(gridData,positionData))
			lastTime = time.time()



######################
#PROGRAM STARTS HERE!#
######################

main()
