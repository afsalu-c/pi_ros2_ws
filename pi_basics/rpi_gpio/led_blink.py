import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LED_pin = 17
GPIO.setup(LED_pin, GPIO.OUT) # pull_up_down only use for input
print("Press Ctrl+C to terminate")

try:
    while True:
        GPIO.output(LED_pin, GPIO.HIGH)
        time.sleep(1.0)

        GPIO.output(LED_pin, GPIO.LOW)
        time.sleep(1.0)

except KeyboardInterrupt:
    print("Program is stopped by the user")
    GPIO.cleanup() # This function will reset the mode of all pins to input
