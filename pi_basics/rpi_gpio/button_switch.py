#-----------USING PULL UP RESISTOR--------------------

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

button_switch  = 2

GPIO.setup(button_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP) #default state is 1

print("Press Ctrl+C to terminate")

try:
    while True:
        if GPIO.input(button_switch) == GPIO.LOW: #  if button pressed input connects to GND, Reads 0
            print("Butten is pressed")        
        else :

            print("Butten is Released") #  if button not pressed internal resistor pulls 3.3V, Reads 1
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program is stopped by the user")
    GPIO.cleanup()


#-----------USING PULL DOWN (NOT RECCOMENDED)--------------------

# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)

# button_switch  = 17
# GPIO.setup(button_switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #default state is 0

# print("Press Ctrl+C to terminate")

# try:
#     while True:
#         if GPIO.input(button_switch) == GPIO.LOW: 
#             print("Butten is pressed")        
#         else :

#             print("Butten is Released") 
#         time.sleep(0.1)

# except KeyboardInterrupt:
#     print("Program is stopped by the user")
#     GPIO.cleanup()