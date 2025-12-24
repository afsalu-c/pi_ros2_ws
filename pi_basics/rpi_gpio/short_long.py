import RPi.GPIO as GPIO
import time
from threading import Timer

GPIO.setmode(GPIO.BCM)
button_switch = 2
GPIO.setup(button_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

press_start_time = 0
long_press_timer = 0

def on_button_press(channel):
    global press_start_time, long_press_timer
    press_start_time = time.perf_counter()
    print("Button is pressed...")

def on_button_release(channel):
    global press_start_time, long_press_timet
    press_duration = time.perf_counter() - press_start_time


    if press_duration <= 0.25 :
        print(f"Short press ({press_duration:.3f}s)")
    else :
        print(f"Long press ({press_duration:.3f}s)")

GPIO.add_event_detect(button_switch, GPIO.FALLING,
                      callback=on_button_press, bouncetime=50)
GPIO.add_event_detect(button_switch, GPIO.RISING,
                      callback=on_button_release, bouncetime=50)

print("Press Ctrl+C to terminate")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nProgram terminated by user")
    GPIO.cleanup()

