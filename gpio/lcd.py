import RPi.GPIO as GPIO
import time

D4 = 0
D5 = 0
D6 = 0
D7 = 0
RS = 0
EN = 0

def send_cmd(value):
    
        msbits = value>>4    
        
        GPIO.output(RS,False) # Indicate is a command being send
        
        # Send higher bits
        GPIO.output(D4,((msbits>>0) & 0x01)) 
        GPIO.output(D5,((msbits>>1) & 0x01))
        GPIO.output(D6,((msbits>>2) & 0x01))
        GPIO.output(D7,((msbits>>3) & 0x01))
        GPIO.output(EN,False)
        time.sleep(0.000001)
        GPIO.output(EN,True)
        time.sleep(0.000001)
        GPIO.output(EN,False)
        time.sleep(0.001)
        
        # Send lower bits      
        GPIO.output(D4,((value>>0) & 0x01)) 
        GPIO.output(D5,((value>>1) & 0x01))
        GPIO.output(D6,((value>>2) & 0x01))
        GPIO.output(D7,((value>>3) & 0x01))
        GPIO.output(EN,False)
        time.sleep(0.000001)
        GPIO.output(EN,True)
        time.sleep(0.000001)
        GPIO.output(EN,False)
        time.sleep(0.01)
     
def send_char(value):
        
        msbits = value>>4 
        
        GPIO.output(RS,True) # Indicate is a char is being send 
       
        
        # Send higher bits
        GPIO.output(D4,((msbits>>0) & 0x01)) 
        GPIO.output(D5,((msbits>>1) & 0x01))
        GPIO.output(D6,((msbits>>2) & 0x01))
        GPIO.output(D7,((msbits>>3) & 0x01))
        GPIO.output(EN,False)
        time.sleep(0.000001)
        GPIO.output(EN,True)
        time.sleep(0.000001)
        GPIO.output(EN,False)
        time.sleep(0.000001)
        
        # Send lower bits      
        GPIO.output(D4,((value>>0) & 0x01)) 
        GPIO.output(D5,((value>>1) & 0x01))
        GPIO.output(D6,((value>>2) & 0x01))
        GPIO.output(D7,((value>>3) & 0x01))
        GPIO.output(EN,False)
        time.sleep(0.000001)
        GPIO.output(EN,True)
        time.sleep(0.000001)
        GPIO.output(EN,False)
        time.sleep(0.000001)

# Initialize LCD in 4-bit mode, clears screen and setup cursor
def lcd_begin(d4,d5,d6,d7,rs,en):
    global D4
    global D5
    global D6
    global D7
    global RS
    global EN
    
    D4 = d4
    D5 = d5
    D6 = d6
    D7 = d7
    RS = rs
    EN = en
    
    GPIO.setup(D4,GPIO.OUT)
    GPIO.setup(D5,GPIO.OUT)
    GPIO.setup(D6,GPIO.OUT)
    GPIO.setup(D7,GPIO.OUT)
    GPIO.setup(RS,GPIO.OUT)
    GPIO.setup(EN,GPIO.OUT)
    
    # Handshaking process
    time.sleep(0.050)##first try
    send_cmd(0x30)
    time.sleep(0.05)##sencond try
    send_cmd(0x30)
    time.sleep(0.05)##third try
    send_cmd(0x30)
    time.sleep(0.0015)##final go
    send_cmd(0x20)
    
    send_cmd(0x28)## select 4 bit, mode 2 lines ,5x8 font
    lcd_clear()## clear screen
    send_cmd(0x06)## display ON
    send_cmd(0x80)## bring cursor to position 0 of line 1
    send_cmd(0x0C)## turn display ON for cursor blinking
    
def lcd_message(text):
        text = str(text)
        length = len(text)
        for i in range (0,length):
            ascii = ord(text[i])    # Convert text at index position into ASCII #
            send_char(ascii)

def lcd_clear():
        send_cmd(0x01) # Clear screen

def lcd_setCursor(row,col):
    
        col = col-1  
    
        if(row==1):
            pos=0x80       # first position (1,1)
        if(row==2):
            pos=0xC0       # 0x80 + 0x40 = 0xC0
        cursor = pos + col # Add to current row position the column position
        send_cmd(cursor)   
        