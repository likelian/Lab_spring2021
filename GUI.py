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

        self.button1 = QtWidgets.QPushButton("Choose file")
        self.button2 = QtWidgets.QPushButton("Play")
        self.button3 = QtWidgets.QPushButton("Pause")
        #self.button4 = QtWidgets.QPushButton("Play_midi")

        self.gain_dial = QtWidgets.QDial()
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)



        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        #self.layout.addWidget(self.button4)
        self.layout.addWidget(self.gain_dial)

        self.button1.clicked.connect(self.load_file)
        self.button2.clicked.connect(self.play_audio)
        self.button3.clicked.connect(self.pause_audio)
        #self.button4.clicked.connect(self.play_midi)
        #self.gain_dial.valueChanged[int].connect(self.gainChangeValue)
        self.gain_dial.valueChanged.connect(self.gainChangeValue)
        self.gain = 0.5

    @QtCore.Slot()
    def gainChangeValue(self, value):
        self.gain = value / 100

    def load_file(self):
        self.audio_file = str(QtWidgets.QFileDialog.getOpenFileName(self)[0])
        self.text.setText(self.audio_file)
        self.wf = wave.open(self.audio_file, 'rb')
        self.buffer, self.fs = sf.read(self.audio_file)


        def callback(in_data, frame_count, time_info, status):
            #global self.gain
            data = self.wf.readframes(frame_count)
            in_data_nda = np.frombuffer(data, dtype=np.int16)
            output = in_data_nda * self.gain * 0.2
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
        fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax = fig.add_subplot(111)
        ax.plot(self.buffer)
        # generate the canvas to display the plot
        canvas = FigureCanvas(fig)
        self.layout.addWidget(canvas)

        Bassline = Bass.Bass(self.audio_file)
        Bassline.root_onset()


    def play_audio(self):
        self.play_midi()
        self.stream.start_stream()


    def midi(self):

        clock = pygame.time.Clock()
        self.pygame.music.load(("output/midi/bassline.mid"))
        self.pygame.music.play()

        #while self.pygame.music.get_busy():
        #    clock.tick(30) # check if playback has finished

    def play_midi(self):
        # mixer config
        freq = 44100  # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 1  # 1 is mono, 2 is stereo
        buffer = 1024   # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        self.pygame = pygame.mixer
        # optional volume 0 to 1.0
        self.pygame.music.set_volume(1.0)
        # listen for interruptions
        #try:
          # use the midi file you just saved
        self.midi()
        #except KeyboardInterrupt:
          # if user hits Ctrl/C then exit
          # (works only in console mode)
        #raise SystemExit

    def pause_audio(self):
        self.stream.stop_stream()
        self.pygame.music.fadeout(1000)
        self.pygame.music.stop()


    def get_FileName(self):
        return self.audio_file


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()


    sys.exit(app.exec_())
