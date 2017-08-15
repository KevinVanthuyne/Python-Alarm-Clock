import pygame
import os
import random
import time
import datetime
import sys
import re
import tkinter as tk
import threading

# TODO max tijd om af te spelen

__alarmtime = ''  # HH:MM
__path_to_sounds = 'sounds'  # folder containing sounds
__fade_in = 10000  # milliseconds to fade in sound
__blacklist = ['instruments', 'other folder']  # folders with sounds not to start with (don't include main folder)

""" Part 1: input """


def input():
    # TODO controle op input
    global __alarmtime
    input_time = sys.argv[1]

    if not re.match(r'^..:..$', input_time):
        print("Invalid input. Has to be HH:MM")
        return False
    else:
        __alarmtime = input_time
        return True


""" Part 2: alarm """


def howLong(alarmtime):
    """ returns timedelta until given time. Format HH:MM
        source used: https://pastebin.com/GLL6L2B8     """

    now = datetime.datetime.now()  # current date & time

    current_date = datetime.date(getattr(now, 'year'), getattr(now, 'month'), getattr(now, 'day'))
    current_time = datetime.time(getattr(now, 'hour'), getattr(now, 'minute'))
    print("Current time: {} {}".format(current_date, current_time))

    alarmtime = datetime.datetime.strptime(alarmtime, '%H:%M') # makes a datetime object from string as formatted
    alarmtime = datetime.time(getattr(alarmtime, 'hour'), getattr(alarmtime, 'minute')) # converts datetime object in time object

    alarmdatetime = datetime.datetime.combine(current_date, alarmtime) # make alarm datetime object with current date and alarmtime

    # DEBUG to make alarm go off immediately
    if alarmtime == current_time:
        return datetime.timedelta(0)

    if alarmtime < current_time: # if alarmtime before current time, set alarm for next day
        alarmdatetime += datetime.timedelta(hours=24)

    time_to_alarm = alarmdatetime - now

    print("Alarm time: {}".format(alarmdatetime))
    print("Alarm goes of in {} (h:m:s)\n".format(time.strftime('%H:%M:%S', time.gmtime(time_to_alarm.seconds))))

    return   time_to_alarm


""" Part 3: sound """

def initMixer():
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer
    pygame.mixer.init()
    print("Mixer initialised")
    print("volume: {}".format(pygame.mixer.music.get_volume()))
    print("")

def getFiles(path):
    """ lists all folders and files in an array
        every child array represents subfolder """

    entries = os.listdir(path)
    structure = []

    for entry in entries:
        entry = os.path.join(path, entry)

        if os.path.isdir(entry):
            structure.append(getFiles(entry))

        if os.path.isfile(entry):
            structure.append(entry)

    return structure

def selectRandomFiles():
    """ selects 1 random sound per folder """

    all_files = getFiles(__path_to_sounds)
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

def makeBlacklist():
    """ join main path and blacklist folders """
    global __blacklist
    blacklist = []

    for file in __blacklist:
        blacklist.append(os.path.join(__path_to_sounds, file))

    __blacklist = blacklist

def inBlacklist(sound):
    """ checks if sound is in blacklisted folder) """

    path = sound.rsplit('/', 1)[0] # path to file without filename

    return path in __blacklist

def playSounds():
    """ plays 1 sound, waits some time then adds the next until all sounds are playing """

    files = selectRandomFiles()
    playing = [] # sounds already playing

    makeBlacklist()

    # TODO random sleep until next sound
    # fade-in (eerste lang (5min ), daarna random en korter? (1min))
    # maybe fade-out and replace with other sound

    # TODO sommige folder nooit als eerste afspelen (instrument)

    for i in range(len(files)): # for the number of selected sounds

        if i != 0: # first sounds plays immediately, other sounds start later (randomly)
            wait = random.randint(10,20) # seconds to wait
            time.sleep(wait)

        while True: # "do ... while" to make sure sound isn't already selected
            sound = random.choice(files)

            if sound not in playing and not (i == 0 and inBlacklist(sound)):
                playing.append(sound)
                pygame.mixer.Sound(sound).play(loops=-1, fade_ms=__fade_in) # play sound on loop with fade in on start
                print("playing: {}".format(sound))
                break

""" Part 4: Visual feedback & cancel """


class MessageBox(threading.Thread):

    def cancel(self):
        print("Alarm cancelled") # TODO alarm hiermee stoppen
        self.root.destroy()
        exitProgram()

    def __init__(self, alarmtime):
        threading.Thread.__init__(self)
        self.alarmtime = alarmtime
        self.daemon = True
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.title("RasPi Alarm")

        message = "Alarm is set at {}".format(self.alarmtime)
        msg = tk.Label(self.root, padx = 30, pady = 50, text = message)
        msg.pack()

        cancel = tk.Button(self.root, padx = 10, pady = 10, text = "Cancel Alarm", command = self.cancel)
        cancel.pack()

        self.root.mainloop()

def exitProgram():
    raise SystemExit


""" Run """

try:
    input()
    MessageBox(__alarmtime) # seperate thread for message dialog so alarm can continue running

    if input():
        initMixer()
        # determine time to sleep and sleep until alarm time
        wait = howLong(__alarmtime).seconds
        time.sleep(wait)
        # make alarm go off
        print("Time to wake up!")
        playSounds()
        print("")

        while pygame.mixer.get_busy():
            print("afspelen")
            time.sleep(5)
    #else:


except (KeyboardInterrupt, SystemExit):
    #pygame.mixer.stop() # ctrl - c voor afsluiten
    print("afspelen gestopt")

except IndexError:
    print("Can't set alarm. Time needs to be given")
