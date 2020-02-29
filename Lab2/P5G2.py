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

A = 18 # opto switch 1 - inner ring
B = 12 # opto switch 2 - outer ring

up_index = 0 # indexes for the list
down_index = 1

A_old = 0
A_new = 0

B_old = 0
B_new = 0

direction = 0

m_list = ['Message 0',
          'Message 1',
          'Message 2',
          'Message 3',
          'Message 4',
          'Message 5',
          'Message 6',
          'Message 7',
          'Message 8',
          'Message 9',
          'Message 10',
          'Message 11',
          'Message 12',
          'Message 13',
          'Message 14',
          'Message 15',]

msbit = 0x00                 # Used for 4-bit interfacing

lookup_list = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]

def fill_lcd_screen(firstRow, secondRow):
    lcd.lcd_clear()
    lcd.lcd_message(firstRow)
    lcd.send_cmd(0xC0)
    lcd.lcd_message(secondRow)
    

def ISR(pin):
    global A_new 
    global B_new
    
    global A_old
    global B_old
    
    global direction
    global up_index
    global down_index
    
    print('\nPin ', pin, ' entered\n')
    
    A_new = GPIO.input(A)
    B_new = GPIO.input(B)
    
    binary_code = (A_old << 3) | (B_old << 2) | (A_new << 1) | B_new
    direction = lookup_list[binary_code]
    
    
    A_old = A_new
    B_old = B_new
    
    if direction > 0: # Clockwise
        up_index = down_index
        down_index = down_index + 1
        
        if(down_index > 15):
            down_index = 0
        
    elif direction < 0: # Counter Clockwise
        down_index = up_index
        up_index = up_index - 1
        
        if(up_index < 0):
            up_index = 15
    
    else:
        return
    
    print('up index: ', up_index)
    print('down index: ', down_index)
    
    fill_lcd_screen(m_list[up_index], m_list[down_index])
          
        
    
def main():
 GPIO.setwarnings(False)
 GPIO.setmode(GPIO.BCM)
 
 GPIO.setup(A,GPIO.IN)
 GPIO.setup(B,GPIO.IN)
 
 lcd.lcd_begin(D4,D5,D6,D7,RS,EN)
 lcd.send_cmd(0x0C)
 fill_lcd_screen(m_list[up_index], m_list[down_index])
 
 GPIO.add_event_detect(A, GPIO.BOTH, ISR, bouncetime = 200) # Setup interrupt to button pin, H->L, ISR, debounce time
 GPIO.add_event_detect(B, GPIO.BOTH, ISR, bouncetime = 200) # Setup interrupt to button pin, H->L, ISR, debounce time
 
 while True:
     time.sleep(1)
     
         
if __name__ == "__main__":
    main()


