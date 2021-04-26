from mido import Message, MidiFile, MidiTrack
import numpy as np

def midi_cut(midi_file, boundaries):
    mid = MidiFile(midi_file)
    boundaries_tick = np.array(boundaries[1:]) * 960

    for i, track in enumerate(mid.tracks):

        mid_new = MidiFile()
        track_new = MidiTrack()
        mid_new.tracks.append(track_new)
        track_new.append(Message('program_change', program=33, time=0))

        boundary_count = 1
        ticktime = 0
        remainder_tick = 0
        note = 0
        remainder = False
        for msg in track:

            ticktime += msg.time


            if ticktime >= boundaries_tick[boundary_count]:
                filename = "output/midi/sections/" + "bassline_" + str(boundary_count) + ".mid"
                boundary_count += 1
                mid_new.save(filename)
                if boundary_count >= len(boundaries_tick): break

                remainder = True

                mid_new = MidiFile()
                track_new = MidiTrack()
                mid_new.tracks.append(track_new)
                #remainder_tick = 0
                track_new.append(Message('program_change', program=33, time=0))


            if remainder == True:
                pass

            else:
                remainder_tick = 0

            tick_time = msg.time
            if remainder:
                tick_time = ticktime - boundaries_tick[boundary_count-1]
            if msg.type == 'note_on':
                note = msg.note
                track_new.append(Message(msg.type, note=note, velocity=msg.velocity, time=int(tick_time)))

            elif msg.type == 'note_off':
                track_new.append(Message(msg.type, note=note, velocity=msg.velocity, time=int(tick_time)))

            else:
                track_new.append(msg)

            remainder = False
            #remainder_tick = 0



        filename = "output/midi/sections/" + "bassline_" + str(boundary_count) + ".mid"
        mid_new.save(filename)
