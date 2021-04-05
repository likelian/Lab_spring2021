import numpy as np
import matplotlib.pyplot as plt
import madmom
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.processors import SequentialProcessor
import mido
from mido import Message, MidiFile, MidiTrack
from scipy import signal



def root2midi(filename):
    pass
    """
    root note to midi
    """

    #madmom.audio.chroma.DeepChromaProcessor(fmin=65, fmax=2100, unique_filters=True, models=None, **kwargs)
    dcp = madmom.audio.chroma.DeepChromaProcessor()
    #chroma = dcp('sounds/wawu.wav')
    decode = DeepChromaChordRecognitionProcessor()
    #chords = decode(chroma)

    chordrec = SequentialProcessor([dcp, decode])
    #chords = chordrec('sounds/wawu.wav')
    chords = chordrec(filename)

    np_chords = np.empty((len(chords),3), dtype=object)
    for idx, e in enumerate(chords):
        np_chords[idx] = np.array([e[0], e[1], e[2]], dtype=object)

    np_chords = np_chords.transpose()
    noteOn = np_chords[0]
    noteOff = np_chords[1]


    RBI = madmom.evaluation.chords.chords(np_chords[2]) # ‘root’, ‘bass’, and ‘intervals’

    np_RBI = np.empty((len(chords), 3), dtype=object)
    for idx, e in enumerate(RBI):
        np_RBI[idx] = np.array([e[0], e[1], e[2]], dtype=object)

    np_RBI = np_RBI.transpose()
    roots = np_RBI[0]


    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=33, time=0))
    for idx, e in enumerate(roots):
        pitch = e + 36
        tickStart = noteOn[idx]*125*23/3
        tickEnd = noteOff[idx]*125*23/3
        tickEnd = tickEnd - tickStart
        if idx == 0: pass;
        else: tickStart = tickStart - noteOff[idx-1]*125*23/3
        tickStart = int(tickStart)
        tickEnd = int(tickEnd)
        track.append(Message('note_on', note=pitch, velocity=64, time=tickStart))
        track.append(Message('note_off', note=pitch, velocity=127, time=tickEnd))

    mid.save('output/midi/root.mid')
