from music21 import *

# Crea una nuova partitura
score = stream.Score()

# Crea un nuovo pentagramma per la partitura
piano_staff = stream.Part()

# Assegna le note per il pentagramma del pianoforte
piano_notes = ['E4', 'D4', 'C4', 'D4', 'E4', 'E4', 'E4', 'B3', 'D4', 'C4', 'B3', 'A3', 'B3', 'C4', 'D4', 'E4', 'D4', 'C4', 'B3', 'C4', 'D4', 'E4', 'E4', 'D4', 'D4', 'E4', 'G4', 'G4', 'E4', 'D4', 'C4', 'B3', 'C4', 'D4', 'E4', 'D4', 'C4']

# Assegna la durata per ogni nota
piano_durations = [.5] * 4 + [.25] + [.5] * 3 + [.25] + [.5] * 4 + [.25] + [.5] * 4 + [.25] + [.5] * 4 + [.25] + [.5] * 3 + [.25] + [.5] * 4

# Aggiungi le note al pentagramma del pianoforte
piano_staff.append([note.Note(pn, quarterLength=pd) for pn, pd in zip(piano_notes, piano_durations)])

# Aggiungi il pentagramma del pianoforte alla partitura
score.append(piano_staff)

# Salva la partitura in formato MIDI
mf = midi.translate.streamToMidiFile(score)
mf.open('rick_astley.mid', 'wb')
mf.write()
mf.close()
