import RPi.GPIO as GPIO
import time

#Constants (pins on the board)
MOTOR_A_ENABLE = 26
MOTOR_A_C = 13
MOTOR_A_D = 19

MOTOR_B_ENABLE = 21
MOTOR_B_C = 16
MOTOR_B_D = 20

#The motor class which contains code for controlling the motors
class Motor():
    def __init__(self,enable,C,D):
        self.enable = enable
        self.C = C
        self.D = D
        GPIO.setup(enable,GPIO.OUT)
        GPIO.setup(C,GPIO.OUT)
        GPIO.setup(D,GPIO.OUT)
        self.pwmChannel = GPIO.PWM(enable, 1024)
        self.pwmChannel.start(0)

    #PWM control in percent
    def pwmControl(self,pwm):
        #print('controlling with pwm: ' + str(pwm))
        if(pwm>=0):
            GPIO.output(self.C,False)
            GPIO.output(self.D,True)
        elif(pwm<0):
            GPIO.output(self.C,True)
            GPIO.output(self.D,False)
        #pwm = min(abs(pwm),50) If we want to bound the pwm
        self.pwmChannel.ChangeDutyCycle(abs(pwm))

    #Stops the motors
    def stop(self):
        self.pwmChannel.ChangeDutyCycle(100)
        GPIO.output(self.C,True)
        GPIO.output(self.D,True)
        time.sleep(0.1)

    #Stops the pwm channel but first stops the motors.
    def terminate(self):
        self.stop()
        self.pwmChannel.stop()




def stop():
    motorA.stop()
    motorB.stop()

def terminate():
    motorA.terminate()
    motorB.terminate()
    GPIO.cleanup()


#this code runs at startup.
#We do GPIO setup and initialize the motor objects.
GPIO.setmode(GPIO.BCM)

motorA = Motor(MOTOR_A_ENABLE,MOTOR_A_C,MOTOR_A_D)
motorB = Motor(MOTOR_B_ENABLE,MOTOR_B_C,MOTOR_B_D)
    
    



