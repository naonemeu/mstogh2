from mido import MidiFile, MidiTrack, MetaMessage, Message, merge_tracks

# Load MIDI file
midi_file = MidiFile('notes_gh2.tempmid')

# Create new tracks

band_bass = MidiTrack()
band_bass.append(MetaMessage('track_name', name='BAND BASS'))

guitar_fretmap = MidiTrack()
guitar_fretmap.append(MetaMessage('track_name', name='FRETMAP'))

# Iterate through existing tracks and modify them
for track in midi_file.tracks:
    if track.name == 'PART BASS':
        # Process PART BASS track
        cumulative_time = 0
        for msg in track:
            cumulative_time += msg.time
            if msg.type in ['note_on', 'note_off']:
                # Modify the notes and append them to BAND BASS
                if msg.note in [96]:
                    modified_msg = Message(type=msg.type, note=msg.note - 60, velocity=msg.velocity, time=cumulative_time)
                    band_bass.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
            else:
            # Verify if the event is a track name
                if msg.type != 'track_name':
                # Copy text events to the new track
                    band_bass.append(msg.copy(time=cumulative_time))
                    cumulative_time = 0
                    
                    
    elif track.name == 'PART GUITAR GHL':
        # Process PART GUITAR GHL track
        cumulative_time = 0
        for msg in track:
            cumulative_time += msg.time
            if msg.type in ['note_on', 'note_off']:
                # Modify the notes and append them to GUITAR FRETMAP
                if msg.note == 98:
                    modified_msg = Message(type=msg.type, note=msg.note - 58, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 99:
                    modified_msg = Message(type=msg.type, note=msg.note - 57, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 100:
                    modified_msg = Message(type=msg.type, note=msg.note - 56, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 95:
                    modified_msg = Message(type=msg.type, note=msg.note - 49, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 96:
                    modified_msg = Message(type=msg.type, note=msg.note - 48, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 97:
                    modified_msg = Message(type=msg.type, note=msg.note - 47, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 86:
                    modified_msg = Message(type=msg.type, note=msg.note - 35, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 87:
                    modified_msg = Message(type=msg.type, note=msg.note - 35, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 88:
                    modified_msg = Message(type=msg.type, note=msg.note - 35, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 83:
                    modified_msg = Message(type=msg.type, note=msg.note - 29, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 84:
                    modified_msg = Message(type=msg.type, note=msg.note - 29, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 85:
                    modified_msg = Message(type=msg.type, note=msg.note - 29, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 62:
                    modified_msg = Message(type=msg.type, note=msg.note + 48, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                    
for track in midi_file.tracks:
    if track.name == 'FRETMAP':
        track.name = 'PART GUITAR GHL'
        cumulative_time = 0
    else:
        continue
        
# Add the new tracks to the MIDI file
midi_file.tracks.extend([band_bass, guitar_fretmap])

for track in midi_file.tracks:
    if track.name == 'FRETMAP':
        track.name = 'PART GUITAR GHL'
        cumulative_time = 0
    else:
        continue

# Remove 'PART RHYTHM' track
midi_file.tracks = [track for track in midi_file.tracks if track.name != 'PART DRUMS']

# Save the modified MIDI file
midi_file.save('notes_gh2.tempmid2')