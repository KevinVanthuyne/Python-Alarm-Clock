import sys
import os
import time
import threading
import datetime
from pygame  import mixer

from alarm import Alarm
from popup import Popup

""" Sets an alarm and shows a popup for when the alarm is set.
    At the given time, alarm goes off """

def run():
    try:

        __alarmtime = ''
        __path_to_sounds = 'sounds'
        __fade_in = 10000
        __blacklist = ['instruments', 'other folder']

        input_time = sys.argv[1]  # get alarmtime from command line
        alarm = Alarm(input_time, __path_to_sounds, __fade_in, __blacklist) # seperate thread for message dialog so alarm can continue running

        # Show popup with when alarm is set and cancel option
        popup = Popup(alarm.get_alarmtime())

        # check if alarmtime == current time or if flag file exists to cancel alarm
        while (alarm.now() != alarm.get_alarmtime() and not os.path.isfile("cancel_alarm")):
            print("sleeping until alarm...")
            time.sleep(1)

        # make alarm go off if flag file doesn't exist
        if not os.path.isfile("cancel_alarm"):
            print("Time to wake up!")
            alarm.init_mixer()
            alarm.play_sounds()
            print("")

            while mixer.get_busy():
                print("playing alarm...")
                time.sleep(5)



    except (KeyboardInterrupt, SystemExit):
        # mixer.stop() # ctrl - c to stop alarm
        try:
            os.remove("cancel_alarms")
            print("Deleted flag file")
        except (NameError, FileNotFoundError):
            print("No flag file to delete")

        print("--- Stopped alarm ---")

    except IndexError:
        print("Can't set alarm. Time needs to be given (HH:MM)")

    except ValueError as err:
        print(err)


if __name__ == '__main__':
    run()
