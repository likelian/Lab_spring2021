#!/usr/bin/env python
import sys
import numpy as np
import soundfile as sf
import pyaudio
import wave
import time
from PySide2 import QtCore, QtWidgets, QtGui
import Bass
import pygame
from threading import Timer

from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure



class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.slider_val_list = []

        self.button1 = QtWidgets.QPushButton("Choose file")
        self.button2 = QtWidgets.QPushButton("Start Playing")
        self.button3 = QtWidgets.QPushButton("End Playing")
        self.button4 = QtWidgets.QPushButton("New Bass")
        self.gain_dial = QtWidgets.QDial()
        self.gain_dial.setValue(50)

        self.layout = QtWidgets.QGridLayout(self)

        self.layout.addWidget(self.button1, 0, 0, 1, 3)
        self.layout.addWidget(self.button2, 1, 0)
        self.layout.addWidget(self.button3, 1, 1)


        self.button1.clicked.connect(self.load_file)
        self.button2.clicked.connect(self.play_audio)
        self.button3.clicked.connect(self.pause_audio)
        self.button4.clicked.connect(self.New_midi)
        self.gain_dial.valueChanged.connect(self.gainChangeValue)
        self.gain = 0.5

    @QtCore.Slot()

    def slider1ChangeValue(self, value):
        self.targeted_note_density = 0.2 + 2*value / 100

    def New_midi(self):
        self.Bassline.root_onset(self.targeted_note_density, self.slider_list, self.boundaries)
        self.midi_setup()



    def gainChangeValue(self, value):
        self.gain = value / 100


    def load_file(self):
        self.audio_file = str(QtWidgets.QFileDialog.getOpenFileName(self)[0])
        #self.text.setText(self.audio_file)
        self.wf = wave.open(self.audio_file, 'rb')
        self.buffer, self.fs = sf.read(self.audio_file)
        self.duration = self.wf.getnframes() / self.fs

        self.time = 0 # playback postion in ms

        def callback(in_data, frame_count, time_info, status):

            data = self.wf.readframes(frame_count)
            in_data_nda = np.frombuffer(data, dtype=np.int16)

            output = in_data_nda * self.gain**3 * 3.162278 * 0.5
            output = output.astype(np.int16)

            return output, pyaudio.paContinue

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True,
            stream_callback=callback)
        self.stream.stop_stream()


        # generate the plot
        fig = Figure(figsize=(600,200), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax = fig.add_subplot(111)
        time = np.linspace(0, len(self.buffer) / self.fs, num = len(self.buffer))
        label = ax.set_xlabel('Seconds', fontsize = 10)
        ax.xaxis.set_label_coords(1.05, 0)
        ax.plot(time, self.buffer)


        self.Bassline = Bass.Bass(self.audio_file)

        self.boundaries = self.Bassline.structure()
        LUFS_list = self.Bassline.LUFS(self.boundaries)

        boundaries_labels = np.empty(len(self.buffer))
        boundaries_labels[:] = np.nan
        for i in self.boundaries[1:-1]:
            boundaries_labels[int(i*self.fs)-1] = 1
            boundaries_labels[int(i*self.fs)-2] = -1
        ax.plot(time, boundaries_labels)
        # generate the canvas to display the plot
        canvas = FigureCanvas(fig)
        self.layout.addWidget(canvas, 2, 0, 1, 2)

        self.slider1 = QtWidgets.QSlider()

        self.slider1.valueChanged.connect(self.slider1ChangeValue)
        self.gain_dial.valueChanged.connect(self.gainChangeValue)

        #self.layout.addWidget(self.slider1, 6, 0, 1, 2)

        self.layout.addWidget(self.gain_dial, 2, 2)
        self.layout.addWidget(self.button4, 1, 2)

        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(1, 0)
        self.layout.setRowStretch(2, 2)
        self.layout.setRowStretch(3, 2)
        self.layout.setRowStretch(4, 0)



        self.slider_Dict = {}
        self.play_Dict = {}

        positions = [(0, j) for j in range(len(self.boundaries)-3)]

        Slider_layout = QtWidgets.QGridLayout(self)
        self.slider_list = np.zeros(len(positions))
        Play_layout = QtWidgets.QGridLayout(self)
        self.play_list = np.zeros(len(positions))

        counter = 0
        for position in positions:
            self.slider_Dict[counter] = QtWidgets.QSlider()

            LUFS_val = LUFS_list[counter]
            if LUFS_val > 4:
                LUFS_val = 4
            elif LUFS_val < -4:
                LUFS_val = -4
            slider_val = 52 + int(6 * LUFS_val)

            self.slider_Dict[counter].setValue(slider_val)

            slider_val /= 100
            if slider_val <= 0.3:
                self.slider_list[counter] = 3.25 * slider_val + 0.125
            elif slider_val > 0.3 and slider_val <= 0.8:
                self.slider_list[counter] = 1.5 * slider_val + 0.65
            elif slider_val > 0.8:
                self.slider_list[counter] = 2.5 * slider_val - 0.15

            Slider_layout.addWidget(self.slider_Dict[counter], *position)
            self.slider_Dict[counter].valueChanged.connect(self.slider_slot)


            self.play_Dict[counter] = QtWidgets.QPushButton("Play ("+str(counter+1)+")")
            Play_layout.addWidget(self.play_Dict[counter], *position)
            self.play_Dict[counter].clicked.connect(self.section_midi)

            counter += 1


        self.layout.addLayout(Slider_layout, 3, 0, 1, 3)
        self.layout.addLayout(Play_layout, 4, 0, 1, 3)


        self.targeted_note_density = 1

        self.New_midi()


    def slider_slot(self, value):
        for key, val in self.slider_Dict.items():
            if val == self.sender():
                self.slider_list[key] = 0.125 * 2**(5 * value / 100)


    def play_audio(self):


        def timeout():
            self.pause_audio()

        self.t = Timer(self.duration, timeout)

        self.t.start()

        self.play_midi()
        self.stream.start_stream()




    def play_section_audio(self, pos_start, pos_end):

        self.wf.setpos(int(pos_start*self.fs))

        def timeout():
            self.pause_audio()

        self.t = Timer(pos_end - pos_start, timeout)

        self.pygame.music.play()
        self.stream.start_stream()

        self.t.start()



    def midi_setup(self):
        # mixer config
        freq = 44100  # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 1  # 1 is mono, 2 is stereo
        buffer = 1024   # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        self.pygame_main = pygame.mixer
        # optional volume 0 to 1.0
        self.pygame_main.music.load('output/midi/bassline.mid')
        self.pygame_main.music.set_volume(1.0)


    def section_midi(self):

        for key, val in self.play_Dict.items():

            if val == self.sender():
                freq = 44100  # audio CD quality
                bitsize = -16   # unsigned 16 bit
                channels = 1  # 1 is mono, 2 is stereo
                buffer = 1024   # number of samples
                pygame.mixer.init(freq, bitsize, channels, buffer)
                self.pygame = pygame.mixer

                midi_file = "output/midi/sections/" + "bassline_" + str(key+1) + ".mid"
                self.pygame.music.load(midi_file)
                self.pygame.music.set_volume(1.0)
                start = self.boundaries[key+1]
                end = self.boundaries[key+2]
                if key == 0:
                    start = 0
                self.play_section_audio(start, end)



    def play_midi(self):
        self.midi_setup()
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.pygame_main.music.play()

    def pause_audio(self):
        self.stream.stop_stream()
        self.wf.rewind()

        try:
            self.pygame_main.music.fadeout(1000)
            self.pygame_main.music.stop()
        except:
            pass

        try:
            self.pygame.music.fadeout(1000)
            self.pygame.music.stop()
        except:
            pass

        self.t.cancel()



    def get_FileName(self):
        return self.audio_file

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
