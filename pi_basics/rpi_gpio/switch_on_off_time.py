import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
print("Press Ctrl+C to terminate")

button_switch = 2
GPIO.setup(button_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

timer_start = time.perf_counter()
timer_stop = time.perf_counter()
on_time = float('inf')
off_time = float('-inf')

try :
    while True:
        def check_3() :
            pass

        if GPIO.input(button_switch) == GPIO.LOW:
            timer_start = time.perf_counter()
#            print("Button is pressed")
            on_time = abs(timer_stop - timer_start)
            print("On time : ", on_time)

        if GPIO.input(button_switch) == GPIO.HIGH:
            timer_stop = time.perf_counter()
            off_time = abs(timer_stop - timer_start)
            print("Off time : ", off_time)

            if on_time <= 0.25:
                print("short press")

            if on_time > 0.25 and on_time <= 1.0:
                print("Long press")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nProgram terminated by user")
    GPIO.cleanup()
