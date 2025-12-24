import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

button_switch = 2
LED_pin = 17

GPIO.setup(button_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(button_switch, GPIO.IN)
GPIO.setup(LED_pin, GPIO.OUT)
GPIO.output(LED_pin, GPIO.LOW)

print("Press Ctrl+C to terminate")
count = 0

try:
    while True:
        if GPIO.input(button_switch) == GPIO.LOW:
            count = count + 1

            if count % 2 == 1:
                print("LED ON")
                GPIO.output(LED_pin, GPIO.HIGH)
                time.sleep(0.2)

            else:
                print("LED OFF")
                GPIO.output(LED_pin, GPIO.LOW)
                time.sleep(0.2)
    
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Program is stopped by the user")
    GPIO.cleanup()
