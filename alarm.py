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
    
except KeyboardInterrupt:
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




