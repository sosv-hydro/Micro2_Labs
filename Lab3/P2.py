import sys
sys.path.append('/home/pi/Desktop/Code/Labs')
import RPi.GPIO as GPIO       
import time
from gpio import lcd as lcd
from threading import Thread

# I/O
Buzzer = 26
Button = 21
flag = 19
flag_in = 1

counter = 0
c = 0
duty = .5

#RPI_Freq = 1Ghz approx
#PreScaler = 1024
comp_register = [1952, 975, 650, 487, 324]  #(RPI_Freq)/((PreScaler)(Desired_Freq)) - 1
time_to_wait = [0.002, 0.001, 0.000666666667, 0.0005, 0.0003333333]
freq_used = comp_register[0]                
current_time_delay = time_to_wait[0]                                            


def ChangeFreq(pin):
    global current_time_delay
    global time_to_wait
    global c
    
    if pin == Button:
        current_time_delay = time_to_wait[(c+1)%5]
        print (comp_register[(c+1)%5])
        c = c + 1

def Timer():
    global counter
    global flag
    global freq_used
        
    while True:
        time.sleep(current_time_delay)
        if GPIO.input(flag_in):
            GPIO.output(flag, GPIO.LOW)
        else:
            GPIO.output(flag, GPIO.HIGH)


def Buzz(flag):
    global duty
    
    GPIO.output(Buzzer,GPIO.HIGH)
    time.sleep(current_time_delay * duty)
    GPIO.output(Buzzer,GPIO.LOW)
    
            
def main():
    global Buzzer
    global flag
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(flag, GPIO.OUT)
    GPIO.setup(flag_in, GPIO.IN)
    GPIO.setup(Buzzer, GPIO.OUT)
    GPIO.setup(Button, GPIO.IN)
    GPIO.add_event_detect(flag_in, GPIO.RISING, Buzz)
    GPIO.add_event_detect(Button, GPIO.RISING, ChangeFreq, 200)
    
    T = Thread(target=Timer)
    T.start()
    
    while True:
        time.sleep(1)
            
if __name__ == "__main__":
    main()
