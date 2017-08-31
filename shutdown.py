import RPi.GPIO as GPIO
import time
import os

# default open button needs to be connected to GPIO3 and a Ground pin
# when these pins are shortened, the Pi wakes from a halted state

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN)

def shutdown(self):
    print("Shutting down...")
    GPIO.cleanup()
    time.sleep(1)
    os.system("sudo shutdown -h now")
    
GPIO.add_event_detect(3, GPIO.FALLING, callback=shutdown, bouncetime=2000)

while True:
    time.sleep(5)