#!/usr/bin/env python
import numpy as np
import madmom
from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.processors import SequentialProcessor
import mido
from mido import Message, MidiFile, MidiTrack
from scipy import signal

#import librosa
import msaf

import soundfile as sf
import pyloudnorm as pyln
import aubio
import random
import midi_cut
#from midi2audio import FluidSynth


################################################################################
class Bass(object):
    """docstring for ."""

    def __init__(self, filename):
        #super(, self).__init__()
        self.filename = filename


    def root2midi(self):
        """
        root note to midi
        """

        dcp = madmom.audio.chroma.DeepChromaProcessor()
        decode = DeepChromaChordRecognitionProcessor()
        chordrec = SequentialProcessor([dcp, decode])
        chords = chordrec(self.filename)

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

        return roots, np_chords



    ################################################################################

    def structure(self):
        """
        Structure analysis
        """

        boundaries, labels = msaf.process(self.filename, feature="mfcc", boundaries_id="sf")
        self.boundaries = boundaries
        return boundaries


    ################################################################################

    def LUFS(self, boundaries_original):
        """
        Loudness
        """

        #boundaries = self.structure()

        boundaries = boundaries_original[1:-1]

        data, rate = sf.read(self.filename) # load audio (with shape (samples, channels))
        meter = pyln.Meter(rate) # create BS.1770 meter
        Program_loudness = meter.integrated_loudness(data) # measure loudness
        sec_loudness = []
        for sec_idx in range(len(boundaries)-1):
            sec_data = data[int(boundaries[sec_idx]*rate):int(boundaries[sec_idx+1]*rate)-1]
            if len(sec_data) < rate:
                loudness = -80
            else:
                loudness = meter.integrated_loudness(sec_data) # measure loudness
            sec_loudness.append(loudness - Program_loudness)
        self.LUFS_list = sec_loudness
        return sec_loudness




    ################################################################################

    def beat(self):
        """
        return a list of beat postions
        """

        src = aubio.source(self.filename)

        a_tempo = aubio.tempo(method="default", buf_size=1024, hop_size=512, samplerate=44100)

        total_frames = 0
        beat = []
        while True:
                samples, read = src()
                is_beat = a_tempo(samples)
                if is_beat:
                    this_beat = a_tempo.get_last_s()
                    beat.append(this_beat)

                total_frames += read
                if read < 512:
                    break

        return beat



    ################################################################################

    def onset(self, targeted_note_density=1.5, targeted_note_density_list=[], density_threshold = 0.1):
        """
        onset
        """

        beat = self.beat()

        log_filt_spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram(self.filename, num_bands=24)
        superflux_3 = madmom.features.onsets.superflux(log_filt_spec)


        def density_to_onset(targeted_note_density, superflux_3, beat, density_threshold = 0.1):

            onset_threshold = 7
            step = 0.1
            note_density = 0
            count = 0

            if abs(note_density - targeted_note_density) <= density_threshold:
                density_threshold = targeted_note_density*0.5

            while abs(note_density - targeted_note_density) > density_threshold:
                count += 1
                if count >= 2000: print("note density iterated over 2000"); break;
                difference = note_density - targeted_note_density
                onset_threshold += step * difference
                proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100, threshold=onset_threshold, combine=0.14)

                section_onset = proc(superflux_3)

                note_density = len(section_onset) / len(beat)

                if onset_threshold < 0: print("onset_threshold < 0"); print("note_density", note_density); break

            return section_onset


        onset = np.array([])
        for idx, targeted_note_density in enumerate(targeted_note_density_list):
            left_bound = self.boundaries[1:-1][idx]
            right_bound = self.boundaries[1:-1][idx+1]

            new_superflux_3 = superflux_3[int(left_bound*100) : int(right_bound*100)]

            beat_filter = (beat > left_bound) & (beat < right_bound)
            new_beat = np.array(beat)[beat_filter]

            if targeted_note_density < 0.001:
                targeted_note_density = 0.2

            section_onset = density_to_onset(targeted_note_density, new_superflux_3, new_beat, density_threshold)
            section_onset += left_bound

            onset = np.append(onset, section_onset)


        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        track.append(Message('program_change', program=33, time=0))
        for idx, e in enumerate(onset):
            pitch = 48
            tickStart = onset[idx]*125.4*23/3
            tickEnd = 20
            if idx == 0: pass;
            else: tickStart = tickStart - onset[idx-1]*125.4*23/3 - tickEnd
            tickStart = int(tickStart)
            tickEnd = int(tickEnd)
            track.append(Message('note_on', note=pitch, velocity=64, time=tickStart))
            track.append(Message('note_off', note=pitch, velocity=127, time=tickEnd))

        mid.save('output/midi/onset.mid')

        return onset




    ################################################################################

    def root_onset(self, targeted_note_density, targeted_note_density_list, boundaries):
        """
        Bassline
        Root + Onset
        """
        #targeted_note_density_list
        self.boundaries = boundaries

        onset = self.onset(targeted_note_density, targeted_note_density_list, 0.1)
        roots, np_chords = self.root2midi()
        noteOn = np_chords[0]
        noteOff = np_chords[1]

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

            note_idx = np.searchsorted(noteOn, onset[idx])

            boundaries_idx = np.searchsorted(self.boundaries[1:-1], onset[idx])
            section_vel = int(1.7 * self.LUFS_list[boundaries_idx-1])

            vel = 64 + random.randint(-10, 10) + section_vel
            pitch = roots[note_idx-1]
            if pitch == -1: pitch += 12; vel = 0
            elif 0 <= pitch <= 4: pitch += 36
            else: pitch += 24

            if idx == 0: pass;
            else: tickStart = tickStart - onset[idx-1]*125.4*23/3 - tickEnd_prev
            tickStart = int(tickStart)
            tickEnd = int(tickEnd)
            tickEnd_prev = tickEnd
            track.append(Message('note_on', note=pitch, velocity=vel, time=tickStart))
            track.append(Message('note_off', note=pitch, velocity=127, time=tickEnd))

        mid.save('output/midi/bassline.mid')

        midi_cut.midi_cut('output/midi/bassline.mid', self.boundaries)
        #print(mid)

        #fs = FluidSynth()
        #fs.midi_to_audio('output/midi/bassline.mid', 'ooutput/midi/bassline.wav')
