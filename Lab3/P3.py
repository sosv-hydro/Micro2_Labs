import sys
sys.path.append('/home/pi/Desktop/Code/Labs')
import RPi.GPIO as GPIO       
import time
from gpio import lcd as lcd
from threading import Thread

s_a = 7
s_b = 8
s_c = 25
s_d = 24
s_e = 23
s_f = 15
s_g = 14

segment_array = [s_g, s_f, s_e, s_d, s_c, s_b, s_a]

display_1 = 3 # pin to select 1st display
display_2 = 2 # pin to select 2nd display

dp1 = 27
dp2 = 17

index = 0
flag = 19
flag_in = 1
# Number lookup table
lookup_table = [
#    g,f,e,d,c,b,a
    [1,0,0,0,0,0,0], #0
    [1,1,1,1,0,0,1], #1
    [0,1,0,0,1,0,0], #2
    [0,1,1,0,0,0,0], #3
    [0,0,1,1,0,0,1], #4
    [0,0,1,0,0,1,0], #5
    [0,0,0,0,0,1,0], #6
    [1,1,1,1,0,0,0], #7
    [0,0,0,0,0,0,0], #8
    [0,0,1,0,0,0,0], #9
    [0,0,0,1,0,0,0], #A
    [0,0,0,0,0,1,1], #B
    [1,0,0,0,1,1,0], #C
    [0,1,0,0,0,0,1], #D
    [0,0,0,0,1,1,0], #E
    [0,0,0,1,1,1,0], #F
]

def display7seg(index):
    for i in range(7):
        GPIO.setup(segment_array[i], GPIO.OUT)
        GPIO.output(segment_array[i], lookup_table[index][i])

def ISR(trigger):
    global index
    if trigger == flag_in:
        display7seg(index)
        index = (index + 1)%10

def Timer():
    global flag
    global flag_in

    while True:
        time.sleep(1)
        if GPIO.input(flag_in):
            GPIO.output(flag, GPIO.LOW)
        else:
            GPIO.output(flag, GPIO.HIGH)

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    #setup
    GPIO.setup(display_1, GPIO.OUT)
    GPIO.setup(display_2, GPIO.OUT)
    GPIO.setup(dp1, GPIO.OUT)
    GPIO.setup(dp2, GPIO.OUT)
    GPIO.setup(flag_in, GPIO.IN)
    GPIO.setup(flag, GPIO.OUT)
    #output
    GPIO.output(display_1, GPIO.LOW)
    GPIO.output(display_2, GPIO.LOW)
    GPIO.output(dp1, GPIO.HIGH)
    GPIO.output(dp2, GPIO.HIGH)
    
    GPIO.add_event_detect(flag_in, GPIO.RISING, ISR)
    
    T = Thread(target=Timer)
    T.start()
    
    while True:
        time.sleep(1)
        
if __name__ == "__main__":
    main()
