import mido

spwn_rate = 110 # seuil de vélocité pour considérer un événement comme un spawn
elapsed_time = 0
# chemin relatif vers le fichier MIDI
midi_file = "assets/music/musique1.mid"

def note_to_enemy(note):
    # Exemple de mappage simple
    if  note< 50:
        return "Goblin"
    elif note < 72 and note >= 50:
        return "Orc"
    else:
        return "Dragon"

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
        print(f"Spawn {enemy} à {event['time']} ticks (note: {event['note']}, vélocité: {event['velocity']})")    



