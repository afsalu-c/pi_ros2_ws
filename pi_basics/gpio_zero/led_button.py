from gpiozero import Button, LED
import time

button = Button(2)
led = LED(17)

print("Press Ctrl+C to terminate")

count = 0
while True:
    if button.is_pressed :
        count = count + 1

        if count % 2 == 1:
            print("LED ON")
            led.on()
            time.sleep(0.2)

        else:
            print("LED OFF")
            led.off()
            time.sleep(0.2)

    time.sleep(0.01)

