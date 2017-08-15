import sys
import time
from pygame  import mixer
from alarm import Alarm

""" Sets an alarm and shows a popup for when the alarm is set.
    At the given time, alarm goes off """

try:

    __alarmtime = ''
    __path_to_sounds = 'sounds'
    __fade_in = 10000
    __blacklist = ['instruments', 'other folder']

    input_time = sys.argv[1]  # get alarmtime from command line
    alarm = Alarm(input_time, __path_to_sounds, __fade_in, __blacklist) # seperate thread for message dialog so alarm can continue running
    print("Setting the alarm...")

    # determine time to sleep and sleep until alarm time
    wait = alarm.how_long_until()
    print("wait: " + str(wait))
    time.sleep(wait)

    # make alarm go off
    print("Time to wake up!")
    alarm.init_mixer()
    alarm.play_sounds()
    print("")

    while mixer.get_busy():
        print("playing alarm...")
        time.sleep(5)



except (KeyboardInterrupt, SystemExit):
    #pygame.mixer.stop() # ctrl - c voor afsluiten
    print("--- Stopped alarm ---")

except IndexError:
    print("Can't set alarm. Time needs to be given (HH:MM)")

except ValueError as err:
    print(err)
