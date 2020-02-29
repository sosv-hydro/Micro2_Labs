import sys
sys.path.append('/home/pi/Desktop/Code/Labs')
import RPi.GPIO as GPIO       
import time
from gpio import lcd as lcd

#LCD pins
D4 = 4
D5 = 5
D6 = 6
D7 = 0
RS = 11
EN = 10

#Keypad Column Pins
Col1 = 14
Col2 = 15
Col3 = 16

#keypad Row Pins
Row1 = 23
Row2 = 24
Row3 = 25
Row4 = 8


msbit = 0x00                 # Used for 4-bit interfacing

time_stamp = time.time()

Lookup = [['1','2','3'],
          ['4','5','6'],
          ['7','8','9'],
          ['*','0','#']]

Rows = [Row1, Row2, Row3, Row4]
Columns = [Col1, Col2, Col3]
counter = 0
counter2 = 0

def ScanISR(pin):
    global counter
    global counter2
    global push_flag
    global time_stamp
    
    time_now = time.time()
    
    column = pin-14
    
    if (time_now - time_stamp) >= 0.03: # check if button pin generated interrupt
        
        for row in range(0,4):
            GPIO.output(Rows[row],0)
                  
        for row in range(0,4):
            GPIO.output(Rows[row],GPIO.HIGH)
            if GPIO.input(pin) == GPIO.HIGH:
                message = Lookup[row][column]
                
                if message == "*":
                    lcd.lcd_clear()
                    break
                
                elif message == "#":
                    lcd.send_cmd(0xC0)
                    break
                
                else:
                    counter = counter  +1
                    if(counter == 8):
                        lcd.send_cmd(0xC0)
                        
                    if(counter == 15):
                        lcd.lcd_clear()
                        counter = 0
                    
                    lcd.lcd_message(message)
                    break
                
            GPIO.output(Rows[row],GPIO.LOW)
        
        for row in range(0,4):
            GPIO.output(Rows[row],1)
        
    time_stamp = time_now
    
def main():
 GPIO.setwarnings(False)
 GPIO.setmode(GPIO.BCM)
 
 GPIO.setup(Col1, GPIO.IN)
 GPIO.setup(Col2, GPIO.IN)
 GPIO.setup(Col3, GPIO.IN)
 
 GPIO.setup(Row1, GPIO.OUT)
 GPIO.setup(Row2, GPIO.OUT)
 GPIO.setup(Row3, GPIO.OUT)
 GPIO.setup(Row4, GPIO.OUT)
 
 for row in range(0,4):
    GPIO.output(Rows[row],1)
 
 lcd.lcd_begin(D4,D5,D6,D7,RS,EN)
 lcd.lcd_clear()
 lcd.send_cmd(0x0C)
 lcd.send_cmd(0x0F)
 GPIO.add_event_detect(Col1, GPIO.RISING, ScanISR) # Setup interrupt to button pin, H->L, ISR, debounce time
 GPIO.add_event_detect(Col2, GPIO.RISING, ScanISR)
 GPIO.add_event_detect(Col3, GPIO.RISING, ScanISR)
 
 while True:
     time.sleep(1)
     
         
 

if __name__ == "__main__":
    main()


