import sys
import os
import subprocess
import mido
from mido import MidiFile, MidiTrack, MetaMessage, Message

def FixNoNotes(file_path):
    """Ensure each section has at least one note by adding a placeholder if necessary."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    sections = ["[ExpertDoubleBass]", "[ExpertKeyboard]", "[ExpertDrums]"]
    placeholder_note = "  0 = N 0 0\n"

    modified_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        modified_lines.append(line)

        if line.strip() in sections:
            section_name = line.strip()
            i += 1
            modified_lines.append(lines[i])

            has_notes = False
            i += 1
            while i < len(lines) and lines[i].strip() != "}":
                if "= N" in lines[i]:
                    has_notes = True
                modified_lines.append(lines[i])
                i += 1

            if not has_notes:
                modified_lines.append(placeholder_note)

            if i < len(lines):
                modified_lines.append(lines[i])
        i += 1

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)

def ParseEvents(file_path):
    """Parse the [ExpertSingle], [ExpertDoubleBass], [ExpertKeyboard], and [ExpertDrums] sections for '= E' lines and return events."""
    events_single = []
    events_bass = []
    events_keys = []
    events_drums = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "[ExpertSingle]":
            i += 1
            if i < len(lines) and lines[i].strip() == "{":
                i += 1
                while i < len(lines) and lines[i].strip() != "}":
                    if "= E" in lines[i]:
                        parts = lines[i].strip().split()
                        if len(parts) >= 4 and parts[2] == "E":
                            tick = int(parts[0])
                            event_string = " ".join(parts[3:])
                            events_single.append([tick, event_string])
                    i += 1
        elif line.strip() == "[ExpertDoubleBass]":
            i += 1
            if i < len(lines) and lines[i].strip() == "{":
                i += 1
                while i < len(lines) and lines[i].strip() != "}":
                    if "= E" in lines[i]:
                        parts = lines[i].strip().split()
                        if len(parts) >= 4 and parts[2] == "E":
                            tick = int(parts[0])
                            event_string = " ".join(parts[3:])
                            events_bass.append([tick, event_string])
                    i += 1
        elif line.strip() == "[ExpertKeyboard]":
            i += 1
            if i < len(lines) and lines[i].strip() == "{":
                i += 1
                while i < len(lines) and lines[i].strip() != "}":
                    if "= E" in lines[i]:
                        parts = lines[i].strip().split()
                        if len(parts) >= 4 and parts[2] == "E":
                            tick = int(parts[0])
                            event_string = " ".join(parts[3:])
                            events_keys.append([tick, event_string])
                    i += 1
        elif line.strip() == "[ExpertDrums]":
            i += 1
            if i < len(lines) and lines[i].strip() == "{":
                i += 1
                while i < len(lines) and lines[i].strip() != "}":
                    if "= E" in lines[i]:
                        parts = lines[i].strip().split()
                        if len(parts) >= 4 and parts[2] == "E":
                            tick = int(parts[0])
                            event_string = " ".join(parts[3:])
                            events_drums.append([tick, event_string])
                    i += 1
        i += 1

    return events_single, events_bass, events_keys, events_drums

def ModifyMIDI(midi_file_path, events_single, events_bass, events_keys, events_drums, debug=False):
    """Modify the MIDI file to merge temporary tracks into their respective target tracks while preserving tick timing."""
    midi = MidiFile(midi_file_path)

    # Define track mappings
    track_mappings = [
        (events_single, "PART_GUITAR_TMP", "PART GUITAR"),
        (events_bass, "PART_BASS_TMP", "PART BASS"),
        (events_keys, "PART_KEYS_TMP", "PART KEYS"),
        (events_drums, "PART_DRUMS_TMP", "PART DRUMS"),
    ]

    for events, tmp_track_name, target_track_name in track_mappings:
        # Create the temporary track and add parsed events
        tmp_track = MidiTrack()
        tmp_track.append(MetaMessage('track_name', name=tmp_track_name))
        midi.tracks.append(tmp_track)

        # Add parsed events to the temporary track
        last_event_time = 0
        for event in events:
            tick, event_string = event

            # Calculate delta time
            delta_time = tick - last_event_time
            last_event_time = tick

            # Add event as meta text to the temporary track
            tmp_track.append(MetaMessage('text', text=event_string, time=delta_time))

        # Find the target track
        target_track = None
        for track in midi.tracks:
            for msg in track:
                if msg.type == 'track_name' and msg.name == target_track_name:
                    target_track = track
                    break
            if target_track:
                break

        if not target_track:
            print(f"Error: '{target_track_name}' track not found in the MIDI file.")
            continue

        # Collect all events from both tracks
        all_events = []

        # Add events from target track (note events)
        current_tick = 0
        for msg in target_track:
            current_tick += msg.time
            all_events.append((current_tick, msg))

        # Add events from temporary track (text events)
        current_tick = 0
        for msg in tmp_track:
            current_tick += msg.time
            all_events.append((current_tick, msg))

        # Sort all events by tick
        all_events.sort(key=lambda x: x[0])

        # Create a new merged track
        merged_track = MidiTrack()
        merged_track.append(MetaMessage('track_name', name=target_track_name))

        # Add events to the merged track with correct delta times
        last_tick = 0
        for tick, msg in all_events:
            delta_time = tick - last_tick
            last_tick = tick

            # Handle text events (from temporary track)
            if msg.is_meta and msg.type == 'text':
                merged_track.append(MetaMessage('text', text=msg.text, time=delta_time))

            # Handle note events (from target track)
            elif msg.type in ['note_on', 'note_off']:
                merged_track.append(Message(msg.type, note=msg.note, velocity=msg.velocity, time=delta_time))

            # Handle other meta messages (e.g., track_name, time_signature, set_tempo)
            elif msg.is_meta:
                if msg.type == 'track_name':
                    # Skip duplicate track name events
                    continue
                elif msg.type == 'time_signature':
                    merged_track.append(MetaMessage('time_signature', numerator=msg.numerator, denominator=msg.denominator, time=delta_time))
                elif msg.type == 'set_tempo':
                    merged_track.append(MetaMessage('set_tempo', tempo=msg.tempo, time=delta_time))
                elif msg.type == 'key_signature':
                    merged_track.append(MetaMessage('key_signature', key=msg.key, time=delta_time))
                else:
                    # Handle other meta messages generically
                    merged_track.append(MetaMessage(msg.type, time=delta_time))

        # Replace the target track with the merged track
        midi.tracks.remove(target_track)
        midi.tracks.append(merged_track)

        # Delete the temporary track unless in debug mode
        if not debug:
            midi.tracks.remove(tmp_track)
            
            
            
            
    # Fix text events in all tracks
    for track in midi.tracks:
        # Check if the current track is the EVENTS track
        is_events_track = any(msg.type == 'track_name' and msg.name == 'EVENTS' for msg in track)
    
        # Iterate through all messages in the track
        for msg in track:
            if msg.is_meta and msg.type == 'text':
                text = msg.text
                # Check if the text is properly enclosed in [ ]
                if not text.startswith('[') or not text.endswith(']'):
                    # Print a warning for missing or malformatted text (only if not in EVENTS track)
                    if not is_events_track:
                        print(f"[Fix Text Events] Malformatted text in '{track.name}': {text}")
                        print(f"It was fixed by the script, but consider fixing it in the chart file. Add [ ] to the text\n")
                    # Add [ ] if missing
                    if not text.startswith('['):
                        text = f"[{text}"
                    if not text.endswith(']'):
                        text = f"{text}]"
                    msg.text = text
  


    # List of valid text events (single-line format)
    valid_events = ["[play]", "[idle]", "[wail_on]", "[wail_off]", "[solo_on]", "[solo_off]", "[sync_wag]", "[sync_head_bang]", "[map HandMap_Default]", "[map HandMap_Linear]", "[map HandMap_NoChords]", "[map HandMap_AllChords]", "[map HandMap_DropD]", "[map HandMap_DropD2]", "[map HandMap_Solo]", "[map StrumMap_Default]", "[map StrumMap_punk]", "[map StrumMap_softpick]", "[map StrumMap_SlapBass]", "[nobeat]", "[half_time]", "[double_time]", "[allbeat]","[half_tempo]","[double_tempo]"]
    
    # Iterate through the PART GUITAR track
    for track in midi.tracks:
        # Find the PART GUITAR track
        if any(msg.type == 'track_name' and msg.name == 'PART GUITAR' for msg in track):
            # Iterate through all messages in the track
            for msg in track:
                if msg.is_meta and msg.type == 'text':
                    text = msg.text.strip()
                    # Check if the text is a valid event
                    if text not in valid_events:
                        print(f"[Check local events] Invalid local event found in PART GUITAR track: {text}\n")
            break  # Exit after processing the PART GUITAR track






    # Track the status of solo, wail, and ow_face events
    event_status = {
        'solo': False,  # Initialize solo status
        'wail': False,  # Initialize wail status
        'ow_face': False,  # Initialize ow_face status
    }
    
    # Iterate through the PART GUITAR track
    for track in midi.tracks:
        # Find the PART GUITAR track
        if any(msg.type == 'track_name' and msg.name == 'PART GUITAR' for msg in track):
            # Iterate through all messages in the track
            for msg in track:
                if msg.is_meta and msg.type == 'text':
                    text = msg.text.strip()
                    # Check if the text is one of the tracked events
                    if text in ['[solo_on]', '[solo_off]', '[wail_on]', '[wail_off]', '[ow_face_on]', '[ow_face_off]']:
                        event_name = text.rsplit('_', 1)[0][1:]  # Extract the event name (e.g., "solo")
                        event_type = text.split('_')[-1][:-1]  # Extract the event type (e.g., "on" or "off")
    
                        # Handle event_on
                        if event_type == 'on':
                            if event_status[event_name]:
                                # Duplicate event_on found (status is already True)
                                print(f"[Check local events] Two '{event_name}_on' in sequence without a '{event_name}_off'.\n!!! WILL CRASH THE GAME IF LEFT UNECHECKED !!!\n")
                            else:
                                event_status[event_name] = True  # Update the status to True
    
                        # Handle event_off
                        elif event_type == 'off':
                            if not event_status[event_name]:
                                # Duplicate event_off found (status is already False)
                                print(f"[Check local events] Two '{event_name}_off' in sequence without a '{event_name}_on'.\n!!!WILL CRASH THE GAME IF LEFT UNECHECKED !!!\n")
                            else:
                                event_status[event_name] = False  # Update the status to False
            break  # Exit after processing the PART GUITAR track
    
    # Save the modified MIDI file
    output_path = midi_file_path.replace(".mid", "_mod.mid")
    midi.save(output_path)
  
  
  
  
  
    # # Rename PART DRUMS to PART DRUMS EOF
    # for track in midi.tracks:
        # # Find the PART DRUMS track
        # for msg in track:
            # if msg.type == 'track_name' and msg.name == 'PART DRUMS':
                # msg.name = 'PART DRUMS EOF'
                # break  # Exit after renaming the track




    # Save the modified MIDI file
    output_path = midi_file_path.replace(".mid", "_mod.mid")
    midi.save(output_path)
    # if debug:
        # print(f"Debug mode: Modified MIDI file saved to {output_path} (temporary tracks not deleted).")
    # else:
        # print(f"Modified MIDI file saved to: {output_path}")
        
    # Delete the intermediate .mid file created by chartconvert
    intermediate_midi_path = midi_file_path
    if os.path.exists(intermediate_midi_path):
        os.remove(intermediate_midi_path)
        # print(f"Deleted intermediate MIDI file: {intermediate_midi_path}")
    else:
        print(f"Intermediate MIDI file not found: {intermediate_midi_path}")
        

def convertmid(file_path):
    """Convert the .chart file to MIDI using chartconvert.exe."""
    output_file = file_path.replace(".chart", ".mid")
    command = f'chartconvert.exe "{file_path}" -o'
    subprocess.run(command, shell=True)
    return output_file

if __name__ == "__main__":
    print('mstogh2 1.2 by FilipinDuMods.\nChartconvert (2019-06-13) by raynebc.\nChartconvert auxiliary tool by Naonemeu.\n')
    
    if len(sys.argv) < 2:
        print("Usage: python fix_parse_modify.py <chart_file> [--debug]")
        sys.exit(1)

    chart_file = sys.argv[1]
    debug_mode = "--debug" in sys.argv

    if not os.path.exists(chart_file):
        print(f"Error: File '{chart_file}' not found.")
        sys.exit(1)

    # Fix missing notes in the chart file
    FixNoNotes(chart_file)

    # Parse events from all sections
    events_single, events_bass, events_keys, events_drums = ParseEvents(chart_file)

    # Convert the chart file to MIDI
    midi_file_path = convertmid(chart_file)
    
    print('\n------------------------------------- Warning List -------------------------------------\n')
    # Modify the MIDI file to add the parsed events
    ModifyMIDI(midi_file_path, events_single, events_bass, events_keys, events_drums, debug=debug_mode)
    print('---------------------------------- End Warning List ------------------------------------')
    print('Saved MIDI')

    # print("Processing complete.")