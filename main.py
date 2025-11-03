import pygame
import time
file_path = "assets/music/musique1.mid"
startTime = time.time()
currentTime = time.time() - startTime


pygame.mixer.init()
pygame.mixer.music.load(file_path)
pygame.mixer.music.play()


