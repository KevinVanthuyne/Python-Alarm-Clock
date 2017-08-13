import pygame, os

filename = os.path.join('sounds', 'water.mp3')

pygame.init() 
#pygame.mixer.init(44100, -16, 2, 2048) # setup mixer
pygame.mixer.init(channels=5) # 5 kanalen voor music
clock = pygame.time.Clock()

print(filename)import pygame, os, random, time

__path_of_sounds = 'sounds'

def initMixer():
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer
    pygame.mixer.init()
    print("Mixer initialised")
    print("volume: {}".format(pygame.mixer.music.get_volume()))

def getFiles(path):
    entries = os.listdir(path)
    files = []
    
    for entry in entries:
        entry = os.path.join(path, entry)
        if os.path.isfile(entry):
            files.append(entry)
            
    return files

def selectRandomFiles():
    # TODO mappen structuur en 1 sound per map nemen
    
    all_files = getFiles(__path_of_sounds)
    number = random.randint(1, len(all_files)) # random number of sounds between 1 and all sounds
    print("Number of sounds chosen: {}".format(number))
    
    # randomly select number of sounds from all sound files
    selected_files = []
    
    for i in range(number):
        while True: # "do ... while" to make sure sound isn't already selected
            file = random.choice(all_files)
            
            if file not in selected_files:
                selected_files.append(file)
                print("selected file: {}".format(file))
                break
            
    return selected_files

def playSounds():
    files = selectRandomFiles()
    
    # TODO random sleep until next sound
    # fade-in (eerste lang (5min ), daarna random en korter? (1min))
    # maybe fade-out and replace with other sound
    for file in files:
        sound = pygame.mixer.Sound(file)
        sound.play(loops=-1, fade_ms=1000) # fade_ms=60000
    

try:
    initMixer()
    playSounds()
    
    while pygame.mixer.get_busy():
        print("afspelen")
        time.sleep(5)
    
except KeyboardInterrupt:import pygame, os, random, time, datetime

__alarmtime = '22:11' # HH:MM
__path_to_sounds = 'sounds' #folder containing sounds
__fade_in = 60000 # milliseconds to fade in sound
__blacklist = ['instruments', 'other folder'] # folders with sounds not to start with (don't include main folder)

""" Part 1: alarm """

def howLong(alarmtime):
    """ returns timedelta until given time. Format HH:MM
        source used: https://pastebin.com/GLL6L2B8     """
    
    now = datetime.datetime.now() # current date & time
    
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
    

""" Part 2: sound """

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
            wait = random.randint(30,60) # seconds to wait
            time.sleep(wait)
        
        while True: # "do ... while" to make sure sound isn't already selected
            sound = random.choice(files)
            
            if sound not in playing and not (i == 0 and inBlacklist(sound)):
                playing.append(sound)
                pygame.mixer.Sound(sound).play(loops=-1, fade_ms=__fade_in) # play sound on loop with fade in on start                
                print("playing: {}".format(sound))
                break

try:
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
    
except KeyboardInterrupt:
    pygame.mixer.stop() # ctrl - c voor afsluiten
    print("afspelen gestopt")





    pygame.mixer.stop() # ctrl - c voor afsluiten
    print("afspelen gestopt")





print("Pygame initialised")
print("volume: {}".format(pygame.mixer.music.get_volume()))

pygame.mixer.music.load(filename)
pygame.mixer.music.play()

try:
    while pygame.mixer.music.get_busy():
        print("afspelen")
        clock.tick(1)
except KeyboardInterrupt:
    pygame.mixer.music.stop() # ctrl - c voor afsluiten
    print("afspelen gestopt")




