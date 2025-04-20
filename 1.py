from mido import MidiFile, MidiTrack, MetaMessage, Message, merge_tracks

# Load MIDI file
midi_file = MidiFile('notes.mid')

# Create new tracks
band_drums_track = MidiTrack()
band_drums_track.append(MetaMessage('track_name', name='BAND DRUMS'))

temp_bass = MidiTrack()
temp_bass.append(MetaMessage('track_name', name='PART BASS'))

temp_rhythm = MidiTrack()
temp_rhythm.append(MetaMessage('track_name', name='PART RHYTHM'))

temp_coop = MidiTrack()
temp_coop.append(MetaMessage('track_name', name='PART GUITAR COOP'))

triggers_track = MidiTrack()
triggers_track.append(MetaMessage('track_name', name='TRIGGERS'))

temp_guitar = MidiTrack()
temp_guitar.append(MetaMessage('track_name', name='PART GUITAR'))

# Iterate through existing tracks and modify them
for track in midi_file.tracks:
    cumulative_time = 0
    
    if track.name == 'PART KEYS':
        # Process PART KEYS track
        for msg in track:
            cumulative_time += msg.time
            if msg.type in ['note_on', 'note_off']:
                # Modify the notes and append them to TRIGGERS
                if msg.note in [96, 97, 98]: #Keyframes: KEYS EXPERT G R Y -> note 48-50 in TRIGGERS (single notes)
                    modified_msg = Message(type=msg.type, note=msg.note - 48, velocity=msg.velocity, time=cumulative_time)
                    triggers_track.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 99:  #World Venue: KEYS EXPERT B -> note 52 in TRIGGERS (Either single note or sustain works)
                    modified_msg = Message(type=msg.type, note=msg.note - 47, velocity=msg.velocity, time=cumulative_time)
                    triggers_track.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                    
                    
    #sorry for the extra gambiarra
    elif track.name == 'PART DRUMS':
        # Process PART DRUMS track
        cumulative_time = 0
        for msg in track:
            cumulative_time += msg.time
            if msg.type in ['note_on', 'note_off']:
                # Modify the notes and append them to BAND DRUMS
                if msg.note == 98: #kick
                    modified_msg = Message(type=msg.type, note=36, velocity=msg.velocity, time=cumulative_time)
                    band_drums_track.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 96: #cymbal
                    modified_msg = Message(type=msg.type, note=37, velocity=msg.velocity, time=cumulative_time)
                    band_drums_track.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
            else:
                # Verify if the event is a track name
                if msg.type != 'track_name':
                    # Copy text events to the new track
                    band_drums_track.append(msg.copy(time=cumulative_time))
                    cumulative_time = 0

    # elif track.name == 'PART DRUMS':
        # # Process PART DRUMS track
        # cumulative_time = 0
        # for msg in track:
            # cumulative_time += msg.time
            # if msg.type in ['note_on', 'note_off']:
                # # Modify the notes and append them to BAND DRUMS
                # if msg.note == 96: #kick
                    # modified_msg = Message(type=msg.type, note=msg.note - 60, velocity=msg.velocity, time=cumulative_time) #36
                    # band_drums_track.append(modified_msg)
                    # cumulative_time = 0  # Reset time after each note is added
                # elif msg.note == 100: #cymbal
                    # modified_msg = Message(type=msg.type, note=msg.note - 63, velocity=msg.velocity, time=cumulative_time) #37
                    # band_drums_track.append(modified_msg)
                    # cumulative_time = 0  # Reset time after each note is added
            # else:
                # # Verify if the event is a track name
                # if msg.type != 'track_name':
                    # # Copy text events to the new track
                    # band_drums_track.append(msg.copy(time=cumulative_time))
                    # cumulative_time = 0
                
    elif track.name == 'PART BASS':
        # Process PART BASS track
        cumulative_time = 0
        for msg in track:
            cumulative_time += msg.time
            if msg.type in ['note_on', 'note_off']:
                # Modify the notes and append them to BAND BASS
                if msg.note in [96, 97, 98, 99, 100, 60, 61, 62, 63, 64, 72, 73, 74, 75, 76, 84, 85, 86, 87, 88]:
                    modified_msg = Message(type=msg.type, note=msg.note, velocity=msg.velocity, time=cumulative_time)
                    temp_bass.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 116:
                    # Define the target notes
                    target_notes = [103, 91, 79, 67]
                    # Copy and paste the note 116 into each of the target notes
                    for target_note in target_notes:
                        modified_msg = Message(type=msg.type, note=target_note, velocity=msg.velocity, time=cumulative_time)
                        temp_bass.append(modified_msg)
                        cumulative_time = 0  # Reset time after all notes are added
            else:
            # Verify if the event is a track name
                if msg.type != 'track_name':
                # Copy text events to the new track
                    temp_bass.append(msg.copy(time=cumulative_time))
                    cumulative_time = 0
                            
                # Remove 'PART BASS' track
                midi_file.tracks = [track for track in midi_file.tracks if track.name != 'PART BASS']
                
    elif track.name == 'PART RHYTHM':
        # Process PART RHYTHM track
        cumulative_time = 0
        for msg in track:
            cumulative_time += msg.time
            if msg.type in ['note_on', 'note_off']:
                # Modify the notes and append them to TEMP RHYTHM
                if msg.note in [96, 97, 98, 99, 100, 60, 61, 62, 63, 64, 72, 73, 74, 75, 76, 84, 85, 86, 87, 88]:
                    modified_msg = Message(type=msg.type, note=msg.note, velocity=msg.velocity, time=cumulative_time)
                    temp_rhythm.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 116:
                    # Define the target notes
                    target_notes = [103, 91, 79, 67]
                    # Copy and paste the note 116 into each of the target notes
                    for target_note in target_notes:
                        modified_msg = Message(type=msg.type, note=target_note, velocity=msg.velocity, time=cumulative_time)
                        temp_rhythm.append(modified_msg)
                        cumulative_time = 0  # Reset time after all notes are added
            else:
            # Verify if the event is a track name
                if msg.type != 'track_name':
                # Copy text events to the new track
                    temp_rhythm.append(msg.copy(time=cumulative_time))
                    cumulative_time = 0
                            
                # Remove 'PART RHYTHM' track
                midi_file.tracks = [track for track in midi_file.tracks if track.name != 'PART RHYTHM']
                
    elif track.name == 'PART GUITAR COOP':
        # Process PART GUITAR COOP track
        cumulative_time = 0
        for msg in track:
            cumulative_time += msg.time
            if msg.type in ['note_on', 'note_off']:
                # Modify the notes and append them to TEMP COOP
                if msg.note in [96, 97, 98, 99, 100, 60, 61, 62, 63, 64, 72, 73, 74, 75, 76, 84, 85, 86, 87, 88]:
                    modified_msg = Message(type=msg.type, note=msg.note, velocity=msg.velocity, time=cumulative_time)
                    temp_coop.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 116:
                    # Define the target notes
                    target_notes = [103, 91, 79, 67]
                    # Copy and paste the note 116 into each of the target notes
                    for target_note in target_notes:
                        modified_msg = Message(type=msg.type, note=target_note, velocity=msg.velocity, time=cumulative_time)
                        temp_coop.append(modified_msg)
                        cumulative_time = 0  # Reset time after all notes are added
            else:
            # Verify if the event is a track name
                if msg.type != 'track_name':
                # Copy text events to the new track
                    temp_rhythm.append(msg.copy(time=cumulative_time))
                    cumulative_time = 0
                            
                # Remove 'PART RHYTHM' track
                midi_file.tracks = [track for track in midi_file.tracks if track.name != 'PART GUITAR COOP']
                
    elif track.name == 'PART GUITAR':
        # Process PART GUITAR track
        cumulative_time = 0
        for msg in track:
            cumulative_time += msg.time
            if msg.type in ['note_on', 'note_off']:
                # Modify the notes and append them to TEMP GUITAR
                if msg.note in [96, 97, 98, 99, 100, 60, 61, 62, 63, 64, 72, 73, 74, 75, 76, 84, 85, 86, 87, 88]:
                    modified_msg = Message(type=msg.type, note=msg.note, velocity=msg.velocity, time=cumulative_time)
                    temp_guitar.append(modified_msg)
                    cumulative_time = 0  # Reset time after each note is added
                elif msg.note == 116:
                    # Define the target notes
                    target_notes = [103, 91, 79, 67]
                    # Copy and paste the note 116 into each of the target notes
                    for target_note in target_notes:
                        modified_msg = Message(type=msg.type, note=target_note, velocity=msg.velocity, time=cumulative_time)
                        temp_guitar.append(modified_msg)
                        cumulative_time = 0  # Reset time after all notes are added
            else:
                # Verify if the event is a track name
                if msg.type != 'track_name':
                    # Copy text events to the new track
                    temp_guitar.append(msg.copy(time=cumulative_time))
                    cumulative_time = 0
                
                # Remove 'PART GUITAR' track
                midi_file.tracks = [track for track in midi_file.tracks if track.name != 'PART GUITAR']

# Rename TRACKS
for track in midi_file.tracks:
    if track.name == 'TEMP GUITAR':
        track.name = 'PART GUITAR'
        cumulative_time = 0
    else:
        continue
        
for track in midi_file.tracks:
    if track.name == 'TEMP BASS':
        track.name = 'PART BASS'
        cumulative_time = 0
    else:
        continue
        
for track in midi_file.tracks:
    if track.name == 'TEMP RHYTHM':
        track.name = 'PART RHYTHM'
        cumulative_time = 0
    else:
        continue
        
for track in midi_file.tracks:
    if track.name == 'TEMP COOP':
        track.name = 'PART GUITAR COOP'
        cumulative_time = 0
    else:
        continue

for track in midi_file.tracks:
    if track.name == 'PART KEYS':
        track.name = 'BAND SINGER'
        cumulative_time = 0
        
        # New list to hold non-note events
        non_note_events = []

        for msg in track:
            cumulative_time += msg.time
            if msg.type not in ['note_on', 'note_off']:
                non_note_events.append(msg.copy(time=cumulative_time))
                cumulative_time = 0  # Reset time after each message

        # Clear the track and re-add only non-note events
        track.clear()
        track.extend(non_note_events)
        
# Add the new tracks to the MIDI file
midi_file.tracks.extend([temp_guitar, band_drums_track, temp_bass, triggers_track])

# Save the modified MIDI file
midi_file.save('notes_gh2.tempmid')