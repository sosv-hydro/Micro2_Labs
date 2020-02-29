import sys
sys.path.append('/home/pi/Desktop/Code/Labs')
import RPi.GPIO as GPIO       
import time
from gpio import lcd as lcd

D4 = 4
D5 = 5
D6 = 6
D7 = 0
RS = 11
EN = 10

BUTTON = 21

msbit = 0x00                 # Used for 4-bit interfacing
counter = 0                  # Global counter
push_flag = 0
time_stamp = time.time()

def ISR(pin):
    global counter
    global push_flag
    global time_stamp
    
    time_now = time.time()
    
    if pin == BUTTON and not push_flag and (time_now - time_stamp) >= 0.10: # check if button pin generated interrupt
        push_flag = 1
        counter = counter + 1
        lcd.lcd_clear()
        lcd.lcd_message(str(counter))
        push_flag = 0
        
    time_stamp = time_now
    
def main():
 GPIO.setwarnings(False)
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(BUTTON,GPIO.IN)
 
 global counter
 
 lcd.lcd_begin(D4,D5,D6,D7,RS,EN)
 lcd.send_cmd(0x0C)
 lcd.lcd_message(str(counter))
 GPIO.add_event_detect(BUTTON, GPIO.FALLING,ISR) # Setup interrupt to button pin, H->L, ISR, debounce time
 
 while True:
     time.sleep(1)
     
         
 

if __name__ == "__main__":
    main()

