from gpiozero import Button
import time

button = Button(2)

while True:
    if button.is_pressed:
        print("Button Pressed")
    else:
        print("Button Released")
    time.sleep(0.01)
