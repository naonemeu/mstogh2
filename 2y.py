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
                if msg.note in [96]: #Speaker Cones
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
                
                #GHL EXPERT
                if msg.note == 95:  # msg.note 98
                    modified_msg = Message(type=msg.type, note=40, velocity=msg.velocity, time=cumulative_time) #40
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 96:  # msg.note 99
                    modified_msg = Message(type=msg.type, note=41, velocity=msg.velocity, time=cumulative_time) #42
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 97:  # msg.note 100
                    modified_msg = Message(type=msg.type, note=42, velocity=msg.velocity, time=cumulative_time) #44
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 98:  # msg.note 95
                    modified_msg = Message(type=msg.type, note=43, velocity=msg.velocity, time=cumulative_time) #46
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 99:  # msg.note 96
                    modified_msg = Message(type=msg.type, note=44, velocity=msg.velocity, time=cumulative_time) #48
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 100:  # msg.note 97
                    modified_msg = Message(type=msg.type, note=45, velocity=msg.velocity, time=cumulative_time) #50
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added

                #GHL HARD
                elif msg.note == 87:  # msg.note 86
                    modified_msg = Message(type=msg.type, note=46, velocity=msg.velocity, time=cumulative_time) #51
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 88:  # msg.note 87
                    modified_msg = Message(type=msg.type, note=47, velocity=msg.velocity, time=cumulative_time) #52
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 92:  # msg.note 88
                    modified_msg = Message(type=msg.type, note=48, velocity=msg.velocity, time=cumulative_time) #53
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 84:  # msg.note 83
                    modified_msg = Message(type=msg.type, note=49, velocity=msg.velocity, time=cumulative_time) #54
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 85:  # msg.note 84
                    modified_msg = Message(type=msg.type, note=50, velocity=msg.velocity, time=cumulative_time) #55
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 86:  # msg.note 85
                    modified_msg = Message(type=msg.type, note=51, velocity=msg.velocity, time=cumulative_time) #56
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                    
                #GHL MEDIUM
                elif msg.note == 75:  # msg.note 86
                    modified_msg = Message(type=msg.type, note=52, velocity=msg.velocity, time=cumulative_time) #51
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 76:  # msg.note 87
                    modified_msg = Message(type=msg.type, note=53, velocity=msg.velocity, time=cumulative_time) #52
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 80:  # msg.note 88
                    modified_msg = Message(type=msg.type, note=54, velocity=msg.velocity, time=cumulative_time) #53
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 72:  # msg.note 83
                    modified_msg = Message(type=msg.type, note=55, velocity=msg.velocity, time=cumulative_time) #54
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 73:  # msg.note 84
                    modified_msg = Message(type=msg.type, note=56, velocity=msg.velocity, time=cumulative_time) #55
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 74:  # msg.note 85
                    modified_msg = Message(type=msg.type, note=57, velocity=msg.velocity, time=cumulative_time) #56
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                    
                #GHL EASY
                elif msg.note == 63:  # msg.note 62
                    modified_msg = Message(type=msg.type, note=58, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 64:  # msg.note 62
                    modified_msg = Message(type=msg.type, note=59, velocity=msg.velocity, time=cumulative_time)
                    guitar_fretmap.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added

                #GHL EASY - BIG NOTE
                elif msg.note == 59:  # msg.note 62
                    modified_msg = Message(type=msg.type, note=62 + 48, velocity=msg.velocity, time=cumulative_time)
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