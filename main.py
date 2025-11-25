import pygame
import time
import mido

from midi_spawn.test_reader import load_spawns

spawns = load_spawns("assets/music/musique1.mid")
print(spawns)

file_path = "assets/music/musique1.mid"

startTime = time.time()
currentTime = time.time() - startTime


# pygame.mixer.init()
# pygame.mixer.music.load(file_path)
# pygame.mixer.music.play()


print("OK")

mid = mido.MidiFile(file_path)

tempo_in_microseconds = None
for msg in mid.tracks[0]:
    if msg.type == 'set_tempo':
        tempo_in_microseconds = msg.tempo
        break
    if tempo_in_microseconds:
        print(f"Tempo found: {tempo_in_microseconds} microseconds per beat")
    else:
        print("No tempo message found; using default tempo of 500000 microseconds per beat")
        tempo_in_microseconds = 500000  # Default tempo (120 BPM)


ticks_per_beat = mid.ticks_per_beat
seconds_per_tick = (tempo_in_microseconds / 1_000_000) / ticks_per_beat
print(seconds_per_tick)

