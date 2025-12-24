from gpiozero import Button, LED
from signal import pause
import threading
from threading import Timer
from time import sleep

button = Button(2, bounce_time=0.05, hold_time=0.42)
led = LED(17)

press_count = 0
held = False
timer = None

led_mode = "OFF"
running = True

MULTI_PRESS_TIMEOUT = 0.45  # seconds

def led_controller():
    global led_mode

    while running:
        if led_mode == "SHORT":
            led.on()
            sleep(0.2)
            led.off()
            sleep(1.0)

        elif led_mode == "DOUBLE":
            led.on()
            sleep(0.2)
            led.off()
            sleep(0.25)
            led.on()
            sleep(0.2)
            led.off()
            sleep(1)

        elif led_mode == "TRIPLE":
            led.on()
            sleep(0.2)
            led.off()
            sleep(0.25)
            led.on()
            sleep(0.2)
            led.off() 
            sleep(0.25)
            led.on()
            sleep(0.2)
            led.off()
            sleep(1)

        elif led_mode == "LONG":
            led.on()
            sleep(1.0)
            led.off()
            sleep(1.0)

        else:
            sleep(0.05)

def reset():
    global press_count
    press_count = 0


def evaluate_presses():
    global press_count, led_mode
    if press_count == 1:
        print("Short press detected\n")
        led_mode = "SHORT"        
    elif press_count == 2:
        print("Double press detected\n")
        led_mode = "DOUBLE"
    elif press_count == 3:
        print("Triple press detected\n")
        led_mode = "TRIPLE"  
    reset()


def on_press():
    global press_count, timer

    press_count += 1

    # Restart timer on every press
    if timer:
        timer.cancel()

    timer = Timer(MULTI_PRESS_TIMEOUT, evaluate_presses)
    timer.start()


def on_hold():
    global held, timer, led_mode
    # held = True

    if timer:
        timer.cancel()

    print("Long press detected\n")
    led_mode = "LONG"
    reset()


# def on_release():
#     global held
#     held = False


led_thread = threading.Thread(target=led_controller)
led_thread.start()

button.when_pressed = on_press
button.when_held = on_hold
#button.when_released = on_release

print("Press Ctrl+C to exit")
pause()




























