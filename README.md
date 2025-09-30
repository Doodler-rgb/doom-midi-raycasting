# doom-midi-raycasting
on lit les evenements du fichier midic avec:
 for i, track in enumerate(mid.tracks):
    print(f"\n--- Piste {i} ---")
    for msg in track:
        print(msg)

ce qui nous donne des messages de ce style: note_on channel=8 note=59 velocity=86 time=0
on prend seulement les notes avec velocity >0

Dans les messages MIDI, time est exprimé en ticks depuis l’événement précédent, pas en secondes absolues.
Autrement dit, ce que l'on obtient a la fin, c'est un delta.

spawn de monstres: en fonction de la velocité: velocity>70 = spawn apres on peut ajouter le fait que, la limite diminue, comme ca plus de spawn.