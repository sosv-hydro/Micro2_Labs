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

BUTTON = 19

msbit = 0x00                 # Used for 4-bit interfacing
counter = 0                  # Global counter

def ISR(pin):
    global counter
    
    if pin == BUTTON: # check if button pin generated interrupt
        counter = counter + 1
        print("counter: ", str(counter) )
        lcd.lcd_clear()
        lcd.lcd_message(str(counter))
        
    
def main():
 GPIO.setwarnings(False)
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(BUTTON,GPIO.IN)
 
 global counter
 
 lcd.lcd_begin(D4,D5,D6,D7,RS,EN)
 lcd.send_cmd(0x0C)
 lcd.lcd_message(str(counter))
 GPIO.add_event_detect(BUTTON, GPIO.FALLING,ISR,200) # Setup interrupt to button pin, H->L, ISR
 
 while True:
     time.sleep(1)
     
         
 

if __name__ == "__main__":
    main()
