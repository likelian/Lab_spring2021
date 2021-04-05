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


filename = input('Enter the filename :')
#sig = madmom.io.audio.load_wave_file(filename, num_channels=1)


"""
Structure analysis
"""


import librosa
import msaf
#import IPython.display

#boundaries, labels = msaf.process(filename)

#audio_file = "msaf-data-master/Sargon/audio/01-Sargon-Mindless.wav"
audio_file = filename

#sr = 44100

#print(msaf.get_all_boundary_algorithms())

#boundaries, labels = msaf.process(filename, sonify_bounds=True, out_bounds=filename, out_sr=sr)
#sonified_file = "my_boundaries.wav"
#boundaries, labels = msaf.process(audio_file)
#boundaries, labels = msaf.process(audio_file, sonify_bounds=True,
#                                    out_bounds=sonified_file, out_sr=sr)

#print(msaf.features_registry)
boundaries, labels = msaf.process(audio_file, feature="cqt", boundaries_id="sf")
print(boundaries)
#print(labels)

#evaluations = msaf.eval.process(audio_file, boundaries_id="foote", labels_id="fmc2d")
#print(evaluations)
#IPython.display.display(evaluations)


#ds_path = "msaf-data-master/Sargon"
#results = msaf.process(ds_path)
#evals = msaf.eval.process(ds_path)
#evals.to_csv(index=False)
#print(evals)


"""
Loudness

LUFS
"""

import soundfile as sf
import pyloudnorm as pyln

data, rate = sf.read(filename) # load audio (with shape (samples, channels))
meter = pyln.Meter(rate) # create BS.1770 meter
Program_loudness = meter.integrated_loudness(data) # measure loudness
sec_loudness = []
print("Program_loudness", Program_loudness)
for sec_idx in range(len(boundaries)-1):
    sec_data = data[int(boundaries[sec_idx]*rate):int(boundaries[sec_idx+1]*rate)-1]
    if len(sec_data) < rate:
        loudness = -60
    else:
        loudness = meter.integrated_loudness(sec_data) # measure loudness
    sec_loudness.append(loudness - Program_loudness)
    print("sec_loudness", loudness - Program_loudness)






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




#######   aubio     ########

import aubio
import numpy as np


src = aubio.source(filename)

a_tempo = aubio.tempo(method="default", buf_size=1024, hop_size=512, samplerate=44100)

total_frames = 0
beat = []
while True:
        samples, read = src()
        is_beat = a_tempo(samples)
        if is_beat:
            this_beat = a_tempo.get_last_s()
            beat.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < 512:
            break


"""
onset
"""

log_filt_spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram(filename, num_bands=24)
#log_filt_spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram("1_umxhq/drums.wav", num_bands=24)

#log_filt_spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram('sounds/Untitled_bass(filtered).wav', num_bands=24)
superflux_3 = madmom.features.onsets.superflux(log_filt_spec)

#proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100, threshold=6, combine=0.15) #threshold!!!!!!
#proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100, threshold=0.7, combine=0.2) #threshold!!!!!!
#onset = proc(superflux_3)

onset_threshold = 7
step = 0.1
targeted_note_density = 1.5
density_threshold = 0.1
note_density = 0
count = 0
if abs(note_density - targeted_note_density) <= density_threshold: density_threshold = targeted_note_density*0.5

while abs(note_density - targeted_note_density) > density_threshold:
    count += 1
    if count >= 2000: print("note density iterated over 2000"); break;
    difference = note_density - targeted_note_density
    #if difference < 1: step *= 5
    onset_threshold += step * difference
    proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100, threshold=onset_threshold, combine=0.15) #threshold!!!!!!
    onset = proc(superflux_3)
    note_density = len(onset) / len(beat)
    if onset_threshold < 0: print("onset_threshold < 0"); print("note_density", note_density); break

    #print("onset_threshold", onset_threshold)
    #print("note_density", note_density)
    #print("difference", difference)
print("count", count)
print("onset_threshold", onset_threshold)
print("note_density", note_density)
print("targeted_note_density", targeted_note_density)




#print(superflux_3)
#plt.plot(superflux_3 / superflux_3.max())  # dotted black
#plt.show()


mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=33, time=0))
for idx, e in enumerate(onset):
    pitch = 48
    tickStart = onset[idx]*125.4*23/3
    #if idx >= len(onset)-1: idx -= 1
    #tickEnd = onset[idx+1]*125*23/3
    tickEnd = 20
    #tickEnd = tickEnd - tickStart
    if idx == 0: pass;
    else: tickStart = tickStart - onset[idx-1]*125.4*23/3 - tickEnd
    tickStart = int(tickStart)
    tickEnd = int(tickEnd)
    track.append(Message('note_on', note=pitch, velocity=64, time=tickStart))
    track.append(Message('note_off', note=pitch, velocity=127, time=tickEnd))

mid.save('output/midi/onset.mid')






"""
Baseline system
Root + Onset
"""

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=33, time=0))
for idx, e in enumerate(onset):


    tickStart = onset[idx]*125.4*23/3
    if idx == len(onset)-1:
        tickEnd = 100
    else:
        tickEnd = (onset[idx+1]*125.4*23/3 - tickStart)*0.8
        #tickEnd = 10000

    note_idx = np.searchsorted(noteOn, onset[idx])

    pitch = roots[note_idx-1]
    if pitch == -1: pitch += 12
    elif 0 <= pitch <= 4: pitch += 48
    else: pitch += 36


    if idx == 0: pass;
    else: tickStart = tickStart - onset[idx-1]*125.4*23/3 - tickEnd_prev
    tickEnd_prev = tickEnd
    tickStart = int(tickStart)
    tickEnd = int(tickEnd)
    #print(tickStart)
    #print(tickEnd)
    track.append(Message('note_on', note=pitch, velocity=64, time=tickStart))
    track.append(Message('note_off', note=pitch, velocity=127, time=tickEnd))

mid.save('output/midi/baseline.mid')






"""
#######1     DBN approximated by a HMM      ########

from madmom.models import BEATS_LSTM

act = madmom.features.beats.RNNBeatProcessor()('sounds/Untitled.wav')
proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
beat = proc(act)
#print(beat)
"""


"""
#######2   CRFBeatDetector     ########

from madmom.models import BEATS_LSTM
from madmom.features.beats_crf import best_sequence

act = madmom.features.beats.RNNBeatProcessor()('sounds/Untitled.wav')
#print(act)
beat = madmom.features.beats_crf.best_sequence(act, 100, 1)[0] / 100
#print(beat)
"""

"""
########3     Constant Tempo is assumed       ########

from madmom.features.beats import BeatDetectionProcessor, RNNBeatProcessor


proc = BeatDetectionProcessor(fps=100)
act = RNNBeatProcessor()('sounds/Untitled.wav')
beat = proc(act)
"""



"""

from madmom.features.beats_hmm import BeatStateSpace

act = madmom.features.beats.RNNBeatProcessor()('sounds/Untitled.wav')
proc = madmom.features.beats_hmm.BeatStateSpace(60, 360)
beat = proc(act)

"""

"""
#######   aubio     ########

import aubio
import numpy as np


src = aubio.source('sounds/Untitled.wav')

a_tempo = aubio.tempo(method="default", buf_size=1024, hop_size=512, samplerate=44100)

total_frames = 0
beat = []
while True:
        samples, read = src()
        is_beat = a_tempo(samples)
        if is_beat:
            this_beat = a_tempo.get_last_s()
            beat.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < 512:
            break

#print(beat)
"""


"""
##################Evaluation of beat detection



#beat = beat[:-1] #remove the one extra


#True_beat = np.arange(288.0) / 2
#True_beat = np.arange(144.0) + 1
#True_beat = (np.arange(288.0) + 1) / 2
True_beat = np.arange(288.0)[4:] / 2

#print(True_beat)

print(beat)
print(True_beat)
error_arr = beat - True_beat
F_score = np.count_nonzero( error_arr < 0.07) / len(error_arr)
mean_error = np.mean(error_arr)
print(F_score)
print(mean_error)

"""


"""
########## beat midi output ##################

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=33, time=0))
for idx, e in enumerate(beat):
    pitch = 36
    tickStart = beat[idx]*125*23/3
    #if idx >= len(onset)-1: idx -= 1
    #tickEnd = onset[idx+1]*125*23/3
    tickEnd = 10
    #tickEnd = tickEnd - tickStart
    if idx == 0: pass;
    else: tickStart = tickStart - beat[idx-1]*125*23/3 - tickEnd
    tickStart = int(tickStart)
    tickEnd = int(tickEnd)
    track.append(Message('note_on', note=pitch, velocity=64, time=tickStart))
    track.append(Message('note_off', note=pitch, velocity=127, time=tickEnd))

mid.save('output/midi/beat.mid')

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
