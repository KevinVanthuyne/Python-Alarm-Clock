import pygame
import os
import random
import time
import datetime
import sys
import re
import tkinter as tk
import threading

""" A Raspberry Pi powered alarm clock that wakes you up with
    a random selection of nature sounds """

class Alarm:

    # TODO max tijd om af te spelen

    def __init__(self, alarmtime, path_to_sounds, fade_in, blacklist):
        # self.__alarmtime = alarmtime  # HH:MM
        self.set_alarmtime(alarmtime)
        self.__path_to_sounds = path_to_sounds  # folder containing sounds
        self.__fade_in = fade_in  # milliseconds to fade in sounds
        self.__blacklist = blacklist  # folders with sounds not to start with (don't include main folder)

    """ Setters """

    def set_alarmtime(self, alarmtime):
        if not re.match(r'^\d\d:\d\d$', alarmtime):
            raise ValueError("Invalid alarmtime input. Has to be HH:MM")
            return False
        else:
            self.__alarmtime = alarmtime
            return True


    """ Alarm """

    def how_long_until(self):
        """ returns amount of seconds from now until alarmtime.
            source used: https://pastebin.com/GLL6L2B8     """

        now = datetime.datetime.now()  # current date & time

        current_date = datetime.date(getattr(now, 'year'), getattr(now, 'month'), getattr(now, 'day'))
        current_time = datetime.time(getattr(now, 'hour'), getattr(now, 'minute'))
        print("Current time: {} {}".format(current_date, current_time))

        self.__alarmtime = datetime.datetime.strptime(self.__alarmtime, '%H:%M') # makes a datetime object from string as formatted
        self.__alarmtime = datetime.time(getattr(self.__alarmtime, 'hour'), getattr(self.__alarmtime, 'minute')) # converts datetime object in time object

        alarmdatetime = datetime.datetime.combine(current_date, self.__alarmtime) # make alarm datetime object with current date and alarmtime

        # DEBUG to make alarm go off immediately
        if self.__alarmtime == current_time:
            return 0

        if self.__alarmtime < current_time: # if alarmtime before current time, set alarm for next day
            alarmdatetime += datetime.timedelta(hours=24)

        time_to_alarm = alarmdatetime - now

        print("Alarm time: {}".format(alarmdatetime))
        print("Alarm goes of in {} (h:m:s)\n".format(time.strftime('%H:%M:%S', time.gmtime(time_to_alarm.seconds))))

        return time_to_alarm.seconds


    """ Part 3: sound """

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
        """ selects 1 random sound per folder """

        all_files = self.get_files(self.__path_to_sounds)
        # number = random.randint(1, len(all_files)) # random number of sounds between 1 and all sounds
        # print("Number of sounds chosen: {}".format(number))

        selected_files = []

        for i in range(0, len(all_files)): # for every folder
            while True: # "do ... while" to make sure sound isn't already selected
                file = random.choice(all_files[i])

                if file not in selected_files:
                    selected_files.append(file)
                    print("selected file: {}".format(file))
                    break

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

        files = self.select_random_files()
        playing = [] # sounds already playing

        self.make_blacklist()

        # TODO random sleep until next sound
        # fade-in (eerste lang (5min ), daarna random en korter? (1min))
        # maybe fade-out and replace with other sound

        for i in range(len(files)): # for the number of selected sounds

            if i != 0: # first sounds plays immediately, other sounds start later (randomly)
                wait = random.randint(10,20) # seconds to wait
                time.sleep(wait)

            while True: # "do ... while" to make sure sound isn't already selected
                sound = random.choice(files)

                if sound not in playing and not (i == 0 and self.in_blacklist(sound)):
                    playing.append(sound)
                    pygame.mixer.Sound(sound).play(loops=-1, fade_ms=self.__fade_in) # play sound on loop with fade in on start
                    print("playing: {}".format(sound))
                    break

    def exit_program():
        raise SystemExit
