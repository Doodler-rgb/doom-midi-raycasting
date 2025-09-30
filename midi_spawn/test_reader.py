import mido

# chemin relatif vers ton fichier MIDI
midi_file = "assets/music/musique1.mid"

# charger le fichier
mid = mido.MidiFile(midi_file)

print("Infos MIDI :")
print(f" - Ticks par battement : {mid.ticks_per_beat}")
print(f" - Nombre de pistes : {len(mid.tracks)}")

# lire les événements
for i, track in enumerate(mid.tracks):
    print(f"\n--- Piste {i} ---")
    for msg in track:
        print(msg)

'''Ce code parcourt toutes les pistes MIDI contenues dans l’objet mid.tracks. 
La fonction Python enumerate est utilisée pour obtenir à la fois l’indice de la piste (i) et l’objet piste lui-même (track).
 À chaque itération, le code affiche un séparateur indiquant le numéro de la piste,
 puis parcourt tous les messages MIDI de cette piste.

La boucle interne for msg in track: affiche chaque message MIDI contenu dans la piste courante.
 Cela permet d’examiner le contenu de chaque piste, message par message,
   ce qui est utile pour déboguer ou analyser la structure d’un fichier MIDI.'''