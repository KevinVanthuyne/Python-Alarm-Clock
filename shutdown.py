import RPi.GPIO as GPIO
import time
import os
from Adafruit_LED_Backpack import SevenSegment

shutdown_pin_nr = 21

# default open button needs to be connected to GPIO3 and a Ground pin
# when these pins are shortened, the Pi wakes from a halted state

GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdown_pin_nr, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def shutdown(self):
    # long press button to shut down
    for i in range(10):
        time.sleep(0.1)
        if GPIO.input(shutdown_pin_nr) == 1: # button not held down
          return

    print("Shutting down...")
    GPIO.cleanup()
    # kill clock script
    os.system("sudo pkill -f 'python /var/www/html/Python-Alarm-Clock/7segment_clock.py'")

    # clear display
    display = SevenSegment.SevenSegment(address=0x70)
    display.begin()
    display.set_brightness(0)
    # display 'OFF'
    display.set_digit_raw(0, 0)
    display.set_digit_raw(1, 63)
    display.set_digit_raw(2, 113)
    display.set_digit_raw(3, 113)
    display.write_display()

    time.sleep(1)

    display.clear()
    display.write_display()

    # remove alarm_set if there is one
    if os.path.isfile("alarm_set"):
        os.remove("alarm_set")
        print("Shutdown: alarm_set removed")

    os.system("sudo shutdown -h now")

GPIO.add_event_detect(21, GPIO.FALLING, callback=shutdown, bouncetime=2000)

while True:
    time.sleep(5)
