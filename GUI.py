import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):

    #file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def __init__(self):
        super().__init__()

        #self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Choose file")

        self.slider = QtWidgets.QSlider()
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.slider)

        self.button.clicked.connect(self.load_file)

    @QtCore.Slot()
    def load_file(self):

        self._audio_file = str(QtWidgets.QFileDialog.getOpenFileName(self)[0])
        self.text.setText(self._audio_file)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
