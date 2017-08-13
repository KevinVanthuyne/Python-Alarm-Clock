import pygame, os

filename = os.path.join('sounds', 'water.mp3')

pygame.init() 
#pygame.mixer.init(44100, -16, 2, 2048) # setup mixer
pygame.mixer.init(channels=5) # 5 kanalen voor music
clock = pygame.time.Clock()

print(filename)
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




