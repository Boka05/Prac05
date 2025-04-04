import RPi.GPIO as GPIO
import time

x=1
numTimes=int(input("Enter total number of tims to blink"))
speed=float(input("Enter length of each blink(sconds):"))
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)

def Blink(numTimes,speed):
    for i in range(0,numTimes):
        GPIO.output(5,True)
        print("Iteration",(i+1))
        
        GPIO.output(10,True)
        print("Iteration",(i+1))
        
        GPIO.output(19,True)
        print("Iteration",(i+1))
        
        GPIO.output(26,True)
        print("Iteration",(i+1))
        
        GPIO.output(29,True)
        print("Iteration",(i+1))
        
        GPIO.output(29,False)
        print("Iteration",(i+1))
        
        GPIO.output(26,False)
        print("Iteration",(i+1))
        
        GPIO.output(19,False)
        print("Iteration",(i+1))
        
        GPIO.output(10,False)
        print("Iteration",(i+1))
        
        GPIO.output(5,False)
        print("Iteration",(i+1))
        time.sleep(speed)
        
Blink(numTimes,speed)
print("Done")
        