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

'''Ce code parcourt toutes les pistes MIDI contenues dans l’objet mid.tracks. 
La fonction Python enumerate est utilisée pour obtenir à la fois l’indice de la piste (i) et l’objet piste lui-même (track).
 À chaque itération, le code affiche un séparateur indiquant le numéro de la piste,
 puis parcourt tous les messages MIDI de cette piste.

La boucle interne for msg in track: affiche chaque message MIDI contenu dans la piste courante.
 Cela permet d’examiner le contenu de chaque piste, message par message,
   ce qui est utile pour déboguer ou analyser la structure d’un fichier MIDI. ligne 28 à 38'''

   spwn_rate = 110 # seuil de vélocité pour considérer un événement comme un spawn
elapsed_time = 0
# chemin relatif vers le fichier MIDI
midi_file = "assets/music/musique1.mid"

# charger le fichier
mid = mido.MidiFile(midi_file)


# lire les événements
for i, track in enumerate(mid.tracks):
    spawns = []
    for msg in track:
      
      elapsed_time += msg.time
      if msg.type == "note_on" and msg.velocity > spwn_rate:
          spawns.append({
          "time": elapsed_time,
          "note": msg.note,
          "velocity": msg.velocity
          })
          # traiter comme un spawn
      print(msg)
    print("================================== ===============================")
    print(spawns)
    for event in spawns:
        enemy = note_to_enemy(event["note"])
        XpltEnemy = []
        print(f"Spawn {enemy} à {event['time']} ticks (note: {event['note']}, vélocité: {event['velocity']})")    

