import pygame
import os
import random
import time
import datetime
import sys
import re
import tkinter as tk
import threading
import signal
import pigpio

""" A Raspberry Pi powered alarm clock that wakes you up with
    a random selection of nature sounds """

class Alarm():

    # TODO maximum time to let alarm play
    # TODO debug check: play entire sound folder to check on errors
    # TODO overall volume fade-in

    def __init__(self, alarmtime, path_to_sounds, fade_in, wait, blacklist, max_sounds, max_time):
        # self.__alarmtime = alarmtime  # HH:MM

        self.set_alarmtime(alarmtime)
        self.__path_to_sounds = path_to_sounds  # folder containing sounds
        self.__fade_in = fade_in  # milliseconds to fade in sounds
        self.__wait = wait # min and max seconds to wait to play next sound
        self.__blacklist = blacklist  # folders with sounds not to start with (don't include main folder)
        self.__max_sounds = max_sounds  # maximum number of sounds to play together
        self.__max_time = max_time  # maximum amount of seconds the alarm plays

        self.gpio = pigpio.pi()

        self.make_alarm_file()
        # check if flag-file to cancel alarm exists and removes it if needed
        if (self.cancel_file_exists()):
            self.remove_cancel_file()



    """ Setters & getters """

    def set_alarmtime(self, alarmtime):
        if not re.match(r'^\d\d:\d\d$', alarmtime):
            raise ValueError("Invalid alarmtime input. Has to be HH:MM")
            return False
        else:
            # makes a datetime object from string as formatted
            self.__alarmtime = datetime.datetime.strptime(alarmtime, '%H:%M')
            # converts datetime object in time object
            self.__alarmtime = datetime.time(getattr(self.__alarmtime, 'hour'), getattr(self.__alarmtime, 'minute'))

            print("Current time: {}".format(self.now()))
            print("Alarm time: {}".format(self.__alarmtime))

            # TODO show difference in time (time -> datetime)
            print("Alarm goes off in {placeholder}")

            return True

    def get_alarmtime(self):
        return self.__alarmtime

    """ Alarm """

    def how_long_until(self):
        """ returns amount of seconds from now until alarmtime.
            source used: https://pastebin.com/GLL6L2B8     """

        # now = datetime.datetime.now()  # current date & time
        #
        # current_date = datetime.date(getattr(now, 'year'), getattr(now, 'month'), getattr(now, 'day'))
        # current_time = datetime.time(getattr(now, 'hour'), getattr(now, 'minute'))
        # print("Current time: {} {}".format(current_date, current_time))
        #
        # self.__alarmtime = datetime.datetime.strptime(self.__alarmtime, '%H:%M') # makes a datetime object from string as formatted
        # self.__alarmtime = datetime.time(getattr(self.__alarmtime, 'hour'), getattr(self.__alarmtime, 'minute')) # converts datetime object in time object
        #
        # alarmdatetime = datetime.datetime.combine(current_date, self.__alarmtime) # make alarm datetime object with current date and alarmtime
        #
        # # DEBUG to make alarm go off immediately
        # if self.__alarmtime == current_time:
        #     return 0
        #
        # if self.__alarmtime < current_time: # if alarmtime before current time, set alarm for next day
        #     alarmdatetime += datetime.timedelta(hours=24)
        #
        # time_to_alarm = alarmdatetime - now
        #
        # print("Alarm time: {}".format(alarmdatetime))
        # print("Alarm goes of in {} (h:m:s)\n".format(time.strftime('%H:%M:%S', time.gmtime(time_to_alarm.seconds))))
        #
        # return time_to_alarm.seconds

        return 5000

    def now(self):
        now = datetime.datetime.now()
        return datetime.time(getattr(now, 'hour'), getattr(now, 'minute'))


    """ Sound """

    def init_mixer(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer
        pygame.mixer.init()
        print("Mixer initialised")
        print("volume: {}".format(pygame.mixer.music.get_volume()))
        print("")

    def get_files(self, path):
        """ lists all folders and files in an array
            every child array represents subfolder """

        entries = os.listdir(path)
        structure = []

        for entry in entries:
            entry = os.path.join(path, entry)

            if os.path.isdir(entry):
                structure.append(self.get_files(entry))

            if os.path.isfile(entry):
                structure.append(entry)

        return structure

    def select_random_files(self):
        """ selects 1 random sound per folder, with a maximum of <__max_sounds> sounds """

        all_files = self.get_files(self.__path_to_sounds)

        one_file_per_folder = []
        selected_files = []

        # select one random sound per folder
        for i in range(0, len(all_files)):
            #while True: # "do ... while" to make sure sound isn't already selected
            file = random.choice(all_files[i])
            one_file_per_folder.append(file)

        # randomly select max number of sounds from all sounds
        for i in range(0, self.__max_sounds):
            file = random.choice(one_file_per_folder)
            selected_files.append(file)
            print("Selected file: {}".format(file))

            one_file_per_folder.remove(file) # remove from list so same file doesn't get picked

        print("File not chosen: {}".format(one_file_per_folder))
        print("")
        return selected_files

    def make_blacklist(self):
        """ join main path and blacklist folders """
        blacklist = []

        for file in self.__blacklist:
            blacklist.append(os.path.join(self.__path_to_sounds, file))

        self.__blacklist = blacklist

    def in_blacklist(self, sound):
        """ checks if sound is in blacklisted folder """

        path = sound.rsplit('/', 1)[0] # path to file without filename

        return path in self.__blacklist

    def play_sounds(self):
        """ plays 1 sound, waits some time then adds the next until all sounds are playing """

        # Stops alarm when max_time is reached
        signal.signal(signal.SIGALRM, self.max_time_handler)
        signal.alarm(self.__max_time)

        # Enables relay to power amplifier
        self.enable_relay()

        files = self.select_random_files()
        playing = [] # sounds already playing

        self.make_blacklist()

        # TODO random sleep until next sound
        # fade-in (eerste lang (5min ), daarna random en korter? (1min))
        # maybe fade-out and replace with other sound

        for i in range(len(files)): # for the number of selected sounds

            if i != 0: # first sounds plays immediately, other sounds start later (randomly)
                wait = random.randint(self.__wait[0],self.__wait[1]) # seconds to wait to play next sound

                # check every 0.2 seconds while waiting if alarm is cancelled
                s = 0
                while s < wait and not self.cancel_file_exists():
                    # check if GPIO cancel button is pressed
                    self.is_button_pressed()

                    time.sleep(0.2)
                    s += 0.2

            # "do ... while" to make sure sound isn't already selected
            # and check if flag file doesn't exist (sleep needs to finish before check can exit loop)
            while True and not self.cancel_file_exists():
                sound = random.choice(files)

                if sound not in playing and not (i == 0 and self.in_blacklist(sound)):
                    playing.append(sound)
                    pygame.mixer.Sound(sound).play(loops=-1, fade_ms=self.__fade_in) # play sound on loop with fade in on start
                    print("playing: {}".format(sound))
                    break

    # Stops alarm when max_time is reached
    def max_time_handler(self, signum, frame):
        self.make_cancel_file()

    def stop_max_time_signal(self):
        signal.alarm(0)

    """ Flag Files """

    def cancel_file_exists(self):
        return os.path.isfile("cancel_alarm")

    def make_cancel_file(self):
        if self.cancel_file_exists():
            print("Cancel file already exists")
        else:
            open("cancel_alarm", "w").close()

    def remove_cancel_file(self):
        os.remove("cancel_alarm")

    # Make a file with the alarmtime in it so
    # the web interface can see when alarm is set
    def make_alarm_file(self):
        if os.path.isfile("alarm_set"):
            raise ValueError("There's already an alarm set")

        with open("alarm_set", 'w') as alarm_file:
            # write alarmtime as HH:MM in file (drop the seconds)
            alarm_file.write(str(self.__alarmtime).rsplit(':', 1)[0])

        print("alarm file made")

    def remove_alarm_file(self):
        os.remove("alarm_set")
        print("alarm file removed")

    """ GPIO cancel button """

    # Setup GPIO button to cancel alarm
    def init_button(self):

        # Pin 18 is connected to button
        self.gpio.set_mode(18, pigpio.INPUT)
        self.gpio.set_pull_up_down(18, pigpio.PUD_UP)

        # Pin 2 is connected to relay
        self.gpio.set_mode(2, pigpio.OUTPUT)
        # hoog zetten?

    def cleanup_button(self):
        self.disable_relay()
        self.gpio.stop()

    def is_button_pressed(self):
        # read input of pin 18
        input = self.gpio.read(18)
        if not input:
            print("button pressed")
            self.make_cancel_file()
            return True

        return False

    # Relay is active low
    def enable_relay(self):
        self.gpio.write(2, 0)

    def disable_relay(self):
        self.gpio.write(2, 1)

    def toggle_relay(self):
        self.gpio.write(2, not self.gpio.read(2))
