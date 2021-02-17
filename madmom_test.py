import numpy as np
import matplotlib.pyplot as plt
import madmom
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.processors import SequentialProcessor
import mido
from mido import Message, MidiFile, MidiTrack

"""
https://github.com/CPJKU/madmom_tutorials/blob/master/audio_signal_handling.ipynb

https://mido.readthedocs.io/en/latest/midi_files.html
"""

#there is both a function and a class performing the same task
    ####sig = madmom.audio.signal.Signal('sounds/wawu.wav')
#sig
#sig.sample_rate

    ####fs = madmom.audio.signal.FramedSignal(sig, frame_size=2048, hop_size=441)
#fs.frame_rate, fs.hop_size, fs[0]

#A reference to the automatically instantiated Signal object is kept as the signal attribute.
#fs.signal

#Complex STFT
    ####stft = madmom.audio.stft.STFT(fs)
#stft[0:2]

#Magnitude Spectrogram
    ####spec = madmom.audio.spectrogram.Spectrogram(stft)
#plt.imshow(spec[:, :200].T, aspect='auto', origin='lower')
    ####spec = madmom.audio.spectrogram.Spectrogram('sounds/wawu.wav', frame_size=2048, hop_size=200, fft_size=4096)
#spec.shape, spec.bin_frequencies
#spec.stft.frames.overlap_factor


#madmom.audio.chroma.DeepChromaProcessor(fmin=65, fmax=2100, unique_filters=True, models=None, **kwargs)
dcp = madmom.audio.chroma.DeepChromaProcessor()
#chroma = dcp('sounds/wawu.wav')
decode = DeepChromaChordRecognitionProcessor()
#chords = decode(chroma)

chordrec = SequentialProcessor([dcp, decode])
#chords = chordrec('sounds/wawu.wav')
chords = chordrec('sounds/Untitled.wav')

np_chords = np.empty((len(chords),3), dtype=object)
for idx, e in enumerate(chords):
    np_chords[idx] = np.array([e[0], e[1], e[2]], dtype=object)

np_chords = np_chords.transpose()
noteOn = np_chords[0]
noteOff = np_chords[1]

#print(noteOn)
#noteOn = np.arange(8) * 1000
#print(noteOn)

RBI = madmom.evaluation.chords.chords(np_chords[2]) # ‘root’, ‘bass’, and ‘intervals’

np_RBI = np.empty((len(chords), 3), dtype=object)
for idx, e in enumerate(RBI):
    np_RBI[idx] = np.array([e[0], e[1], e[2]], dtype=object)

np_RBI = np_RBI.transpose()
roots = np_RBI[0]



mid = MidiFile(type=1)
track = MidiTrack()
mid.tracks.append(track)


track.append(Message('program_change', program=33, time=0))
for idx, e in enumerate(roots):
    pitch = e + 24
    #tickStart = int(1000 * noteOn[idx] * 23/24)
    #tickEnd = int(1000 * noteOff[idx] * 23/24)
    #print(noteOn[idx])
    #tickStart = mido.second2tick(noteOn[idx]/1000, 1, 120)
    #tickEnd = mido.second2tick(noteOff[idx]/1000, 1, 120)
    #tickStart = int(noteOn[idx]*1000/2.604)
    #tickEnd = int(noteOff[idx]*1000/2.604)


    #need to find the correct time scale, not too hard

    
    tickStart = noteOn[idx] * 1000
    tickEnd = noteOff[idx] * 1000
    tickEnd = tickEnd - tickStart
    if idx == 0: pass;
    else: tickStart = tickStart - noteOn[idx-1] * 1000
    tickStart = int(tickStart)
    tickEnd = int(tickEnd)

    #something is wrong with track.append
    track.append(Message('note_on', note=pitch, velocity=64, time=tickStart))
    track.append(Message('note_off', note=pitch, velocity=127, time=tickEnd))


mid.save('output/midi/bass.mid')
