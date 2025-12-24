#gpiozero event-driven programming

from gpiozero import Button
from signal import pause
from time import sleep

button = Button(2, bounce_time=0.05, hold_time=0.25) #bounce_time = 0.05, ignoring next signal untill 50>

was_held = False
#count = 0

def on_press():
    #print("Button is pressed")
    pass

def on_long_press():
    global was_held
    was_held = True
    print("long press detected")
    print()

def on_release_check():
    global was_held
    #global count
  
    if not was_held : 
        #count += 1
        button.wait_for_press(0.25)
        if not button.is_pressed:
            print("short press detected")
            print()
            #count = 0
        else:
        # if  button.is_pressed :
            button.wait_for_press(0.25)
            if not button.is_pressed:
               print("Double press")
               print()
               #count = 1
            else:
                print("Triple press") 
                print()
        # else:
        #     if count % 2 ==  1:
        #         print("short press detected")
        #         print()
        #         count = 0

    was_held = False

button.when_pressed = on_press
button.when_held = on_long_press
button.when_released = on_release_check

print("Press Ctrl+C to exit")
pause() # to keep program alive

