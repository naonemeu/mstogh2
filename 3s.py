from mido import MidiFile, MidiTrack, MetaMessage, Message

# Load the MIDI file
midi_file = MidiFile('notes_gh2.tempmid2')

# Create the new TEMP GUITAR track
temp_guitar = MidiTrack()
temp_guitar.append(MetaMessage('track_name', name='TEMP GUITAR'))

# Function to extract and accumulate events with their absolute time
def accumulate_events(track):
    cumulative_time = 0
    events = []
    for msg in track:
        cumulative_time += msg.time
        # Exclude track_name events
        if not (msg.is_meta and msg.type == 'track_name'):
            # If the message is not a meta message, ensure it's on channel 0
            if not msg.is_meta:
                msg = msg.copy(channel=0)
            events.append((cumulative_time, msg))
    return events

# Extract events from PART GUITAR and PART GUITAR GHL
part_guitar_events = []
part_guitar_ghl_events = []

for track in midi_file.tracks:
    if track.name == 'PART GUITAR':
        part_guitar_events = accumulate_events(track)
    elif track.name == 'PART GUITAR GHL':
        part_guitar_ghl_events = accumulate_events(track)

# Combine and sort events from both tracks by their absolute time
combined_events = sorted(part_guitar_events + part_guitar_ghl_events, key=lambda x: x[0])

# Add the sorted events to the TEMP GUITAR track, adjusting times
previous_time = 0
for time, msg in combined_events:
    # Calculate relative time for the current event
    relative_time = time - previous_time
    temp_guitar.append(msg.copy(time=relative_time))
    previous_time = time

# Remove the original PART GUITAR and PART GUITAR GHL tracks
midi_file.tracks = [track for track in midi_file.tracks if track.name not in ['PART GUITAR', 'PART GUITAR GHL']]

# Add the TEMP GUITAR track to the MIDI file
midi_file.tracks.append(temp_guitar)

for track in midi_file.tracks:
    if track.name == 'TEMP GUITAR':
        track.name = 'PART GUITAR'
        cumulative_time = 0
    else:
        continue
        
for track in midi_file.tracks:
    if track.name == 'BAND SINGER':
        track.name = 'BAND KEYS'
        cumulative_time = 0
    else:
        continue

# Save the modified MIDI file
midi_file.save('notes_gh2.mid')
