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
        __fade_in = 60000
        __wait = [30,60]
        __blacklist = ['instruments', 'other folder']
        __max_sounds = 5

        input_time = sys.argv[1]  # get alarmtime from command line
        alarm = Alarm(input_time, __path_to_sounds, __fade_in, __wait, __blacklist, __max_sounds)
        # Setup GPIO cancel button
        alarm.init_gpio()

        # alarm.test_all_sounds()
        
        # Show popup with when alarm is set and cancel option
        # Not needed when running from php/apache
        # popup = Popup(alarm.get_alarmtime())

        # check if alarmtime == current time or if flag file exists to cancel alarm
        while (alarm.now() != alarm.get_alarmtime() and not alarm.cancel_file_exists()):
            # print("sleeping until alarm...")
            time.sleep(1)

        # make alarm go off if flag file doesn't exist
        if not alarm.cancel_file_exists():
            print("Time to wake up!")
            alarm.init_mixer()
            alarm.play_sounds()
            print("")

            while mixer.get_busy() and not alarm.cancel_file_exists():
                # print("playing alarm...")
                # check if cancel button is pressed
                alarm.is_button_pressed()

                time.sleep(0.2)



    except (KeyboardInterrupt):
        print("--- Stopped alarm ---")

    except IndexError:
        print("Can't set alarm. Time needs to be given (HH:MM)")

    except ValueError as err:
        print(err)

    finally:
        mixer.quit()
        alarm.cleanup_gpio()
        try:
            alarm.remove_cancel_file()
            print("Deleted flag file")
        except (NameError, FileNotFoundError):
            print("No flag file to delete")

        try:
            alarm.remove_alarm_file()
        except (NameError, FileNotFoundError):
            print("No alarm set file to delete")


if __name__ == '__main__':
    run()
