import numpy as np
import matplotlib.pyplot as plt
import madmom

"""
https://github.com/CPJKU/madmom_tutorials/blob/master/audio_signal_handling.ipynb
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

from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor

#madmom.audio.chroma.DeepChromaProcessor(fmin=65, fmax=2100, unique_filters=True, models=None, **kwargs)
dcp = madmom.audio.chroma.DeepChromaProcessor()
#chroma = dcp('sounds/wawu.wav')
decode = DeepChromaChordRecognitionProcessor()
#chords = decode(chroma)

from madmom.processors import SequentialProcessor
chordrec = SequentialProcessor([dcp, decode])
chords = chordrec('sounds/wawu.wav')

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

print(noteOn)
