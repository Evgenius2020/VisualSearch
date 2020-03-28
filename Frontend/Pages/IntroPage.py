from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from Configuration import Configuration


class IntroPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel(Configuration.INTRO_TEXT)
        label.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        label = QLabel(Configuration.KEY_BINDINGS_FORMAT_STRING % ("N", "M"))
        label.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)
