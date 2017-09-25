import pygame
import os
import random
import time
import datetime
import sys
import re
# import tkinter as tk
# import threading
import signal
import pigpio
from Adafruit_LED_Backpack import SevenSegment

""" A Raspberry Pi powered alarm clock that wakes you up with
    a random selection of nature sounds """

class Alarm():

    # TODO overall volume fade-in
    # TODO see log of what is playing/has been played on website
    # TODO setting multiple alarms?
    # TODO press button to see when alarm is set


    # __alarmtime  # time the alarm goes off
    # __path_to_sounds  # folder containing sounds
    # __fade_in  # milliseconds to fade in sounds
    # __wait  # min and max seconds to wait to play next sound
    # __blacklist  # folders with sounds not to start with (don't include main folder)
    # __max_sounds  # maximum number of sounds to play together
    # __max_time  # maximum amount of seconds the alarm plays
    # __volume  # volume of alarm

    def __init__(self, alarmtime, path_to_sounds, fade_in, wait, blacklist, max_sounds):
        # initialise GPIO
        self.gpio = pigpio.pi()

        self.set_alarmtime(alarmtime)
        self.__path_to_sounds = path_to_sounds
        self.__fade_in = fade_in
        self.__wait = wait
        self.__blacklist = blacklist
        self.__max_sounds = max_sounds

        self.make_settings_file()
        self.read_settings()

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


    def now(self):
        now = datetime.datetime.now()
        return datetime.time(getattr(now, 'hour'), getattr(now, 'minute'))


    """ Sound """

    def init_mixer(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer
        pygame.mixer.init()
        self.enable_amplifier()
        print("Mixer initialised")
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

        files = self.select_random_files()
        playing = [] # sounds already playing

        self.make_blacklist()
        # Remove current played sounds file to make new one
        self.remove_played_sounds_file()

        for i in range(len(files)): # for the number of selected sounds

            if i != 0: # first sounds plays immediately, other sounds start later (randomly)
                wait = random.randint(self.__wait[0],self.__wait[1]) # seconds to wait to play next sound

                # check every 0.1 seconds while waiting if alarm is cancelled
                s = 0
                while s < wait and not self.cancel_file_exists():
                    # check if GPIO cancel button is pressed
                    self.is_button_pressed()

                    time.sleep(0.1)
                    s += 0.1

            # "do ... while" to make sure sound isn't already selected
            # and check if flag file doesn't exist (sleep needs to finish before check can exit loop)
            while True and not self.cancel_file_exists():
                sound = random.choice(files)

                if sound not in playing and not (i == 0 and self.in_blacklist(sound)):
                    playing.append(sound)
                    # Make Sound object, set volume and play the sound
                    pygame_sound = pygame.mixer.Sound(sound)
                    pygame_sound.set_volume(self.__volume)
                    pygame_sound.play(loops=-1, fade_ms=self.__fade_in) # play sound on loop with fade in on start

                    print("playing: {}".format(sound))
                    # TODO
                    # add playing sound to file
                    self.add_played_sound(sound)

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

    # makes a settings file with default values if there isn't one yet
    def make_settings_file(self):
        if os.path.isfile("alarm_settings"):
            print("Settings file found")
        else:
            with open("alarm_settings", 'w') as settings_file:
                settings_file.write("volume=1\n")
                settings_file.write("max_time=600")

                print("settings file made")

    # Return the string from an array that matches a substring
    def search_array(self, array, substring):
        for entry in array:
            if substring in entry:
                return entry

    # Reads the settings file and sets variables
    def read_settings(self):
        # put every line of the file in an array
        lines = []

        with open("alarm_settings", "r") as settings_file:
            for line in settings_file:
                lines.append(line)

        # search every setting in settings file and set self.Variables
        volume = self.search_array(lines, "volume").split("=", 1)[1] # get value after =
        self.__volume = float(volume)
        print("volume setting: {}".format(volume.rstrip()))

        max_time = self.search_array(lines, "max_time").split("=", 1)[1]
        self.__max_time = int(max_time)
        print("Max playtime: {}".format(max_time))

    def add_played_sound(self, sound):
        # remove root folder
        sound = sound.split("/", 1)[1]
        # add sound to file
        with open("played_sounds", "a") as played_sounds_file:
            played_sounds_file.write(sound + "\n");

    def remove_played_sounds_file(self):
        if os.path.isfile("played_sounds"):
            os.remove("played_sounds")
            print("played_sounds file removed")
        else:
            print("no played_sounds file found")

    """ GPIO cancel button & amplifier control """

    # Setup GPIO button to cancel alarm and shutdown amplifier
    def init_gpio(self):

        # GPIO13 / pin 33 is connected to stop-alarm button
        self.gpio.set_mode(13, pigpio.INPUT)
        self.gpio.set_pull_up_down(13, pigpio.PUD_UP)

        # GPIO14 / pin 8 is connected to amplifier shutdown
        self.gpio.set_mode(14, pigpio.OUTPUT)
        self.disable_amplifier()

        # GPIO5 / pin 29 is connected to a LED
        self.gpio.set_mode(5, pigpio.OUTPUT)
        # Enable LED to indicate alarm is set
        self.enable_LED()

    def cleanup_gpio(self):
        # self.enable_amplifier()
        self.disable_amplifier()
        # Disable LED to indicate alarm is cancelled
        self.disable_LED()
        self.gpio.stop()

    def check_alarm_button(self):
        input = self.gpio.read(13)
        if not input:
            print("button pressed")
            # show alarm time on display
            segment = SevenSegment.SevenSegment(address=0x70)
            segment.begin()
            segment.set_brightness(0)

            segment.print_number_str("{}{}".format(self.get_alarmtime().hour, self.get_alarmtime().minute))
            segment.set_colon(True)
            segment.write_display()

            time.sleep(1)

    def is_button_pressed(self):
        # read input of pin 13
        input = self.gpio.read(13)
        if not input:
            print("button pressed")
            self.make_cancel_file()
            return True

        return False

    def enable_amplifier(self):
        self.gpio.write(14, 1)

    def disable_amplifier(self):
        self.gpio.write(14, 0)

    def enable_LED(self):
        self.gpio.write(5, 1)

    def disable_LED(self):
        self.gpio.write(5, 0)

    def set_LED(self, state):
        if state == 0 or state == 1:
            self.gpio.write(5, state)


    """ DEBUG """

    # Run this function to test if all sounds are able to be played by Pygame
    def test_all_sounds(self):
        self.init_mixer()

        all_files = self.get_files(self.__path_to_sounds)
        errors = []

        for folder in all_files:
            for file in folder:
                try:
                    print("playing {}".format(file))
                    pygame.mixer.Sound(file).play()
                    pygame.mixer.stop()
                except pygame.error:
                    errors.append(file)

        if errors:
            print("\nCan't play files:")
            for error in errors:
                print(error)
        else:
            print("\nNo errors found, all files can be played!")
