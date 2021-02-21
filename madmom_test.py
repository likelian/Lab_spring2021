import numpy as np
import matplotlib.pyplot as plt
import madmom
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.processors import SequentialProcessor
import mido
from mido import Message, MidiFile, MidiTrack
from scipy import signal

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
chords = chordrec('sounds/Untitled.wav')

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



"""
onset
"""

#log_filt_spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram('sounds/Untitled.wav', num_bands=24)
log_filt_spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram('sounds/Untitled_bass(filtered).wav', num_bands=24)
superflux_3 = madmom.features.onsets.superflux(log_filt_spec)
#proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100, threshold=7, combine=0.25) #threshold!!!!!!
proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100, threshold=0.7, combine=0.2) #threshold!!!!!!
onset = proc(superflux_3)



#print(superflux_3)
#plt.plot(superflux_3 / superflux_3.max())  # dotted black
#plt.show()


mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=33, time=0))
for idx, e in enumerate(onset):
    pitch = 48
    tickStart = onset[idx]*125*23/3
    #if idx >= len(onset)-1: idx -= 1
    #tickEnd = onset[idx+1]*125*23/3
    tickEnd = 20
    #tickEnd = tickEnd - tickStart
    if idx == 0: pass;
    else: tickStart = tickStart - onset[idx-1]*125*23/3 - tickEnd
    tickStart = int(tickStart)
    tickEnd = int(tickEnd)
    track.append(Message('note_on', note=pitch, velocity=64, time=tickStart))
    track.append(Message('note_off', note=pitch, velocity=127, time=tickEnd))

mid.save('output/midi/onset.mid')





"""
beat, very slow...
"""

"""
from madmom.models import BEATS_LSTM

act = madmom.features.beats.RNNBeatProcessor()('sounds/Untitled.wav')
proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
beat = proc(act)
"""






"""
downbeat
"""

"""
#have to give 3/4, 4/4......
proc = madmom.features.beats.DBNDownBeatTrackingProcessor(beats_per_bar=[4, 4], fps=100)
act = madmom.features.beats.RNNDownBeatProcessor()('sounds/Untitled.wav')
downbeat = proc(act)
print(downbeat)
"""
