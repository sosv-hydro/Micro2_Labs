import sys
sys.path.append('/home/pi/Desktop/Code/Labs')
import RPi.GPIO as GPIO       
import time
from gpio import lcd as lcd

Buzzer = 26
counter = 0
c = 0

# RPI_Freq = 1Ghz approx
# PreScaler = 1024
comp_register = [1952, 975, 650, 487, 324]  #(RPI_Freq)/((PreScaler)(Desired_Freq)) - 1
#comp_register = [487, 243, 161, 121, 80]
freq_used = comp_register[0 ]               

time_to_wait = [0.002, 0.001, 0.000666666667, 0.0005, 0.0003333333]
time_used = time_to_wait[0]

duty = .5
button = 21

def ChangeFreq(pin):
    global comp_register
    global freq_used
    global button
    global c
    global counter
    global time_used
    global time_to_wait
    
    
    if pin == button:
        c = c + 1
        freq_used = comp_register[(c)%5]
        time_used = time_to_wait[(c)%5]
        print (comp_register[(c)%5])
        counter = 0

def main():
    global counter
    global Buzzer
    global comp_register
    global duty
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Buzzer, GPIO.OUT)
    GPIO.setup(button, GPIO.IN)
    GPIO.add_event_detect(button, GPIO.FALLING, ChangeFreq,200)
    print (comp_register[c])
    
    while True:
        GPIO.output(Buzzer,GPIO.LOW)
        counter = counter + 1
        
        if counter == freq_used:
            GPIO.output(Buzzer,GPIO.HIGH)
            while counter >= freq_used*duty:
                counter = counter - 1
          #  time.sleep(0.0005)
            GPIO.output(Buzzer,GPIO.LOW)
            counter = 0
            
        
if __name__ == "__main__":
    main()