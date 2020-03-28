from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStackedWidget, QApplication, QFormLayout

from Backend.Bar import Bar
from Frontend.Pages.IntroPage import IntroPage
from Frontend.Pages.TrialPage import TrialPage


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.StackedWidget = QStackedWidget(self)
        self.StackedWidget.addWidget(IntroPage())
        self.trial = TrialPage()
        self.trial.set_bars_to_display([Bar(0, 0, False, False), Bar(3, 3, True, True)])
        self.StackedWidget.addWidget(self.trial)

        self.setStyleSheet("QLabel { color : white; } Application {background-color: black;}")
        self.setCursor(Qt.BlankCursor)

        layout = QFormLayout()
        layout.addWidget(self.StackedWidget)
        self.setLayout(layout)
        self.show()

    def display(self, i):
        self.StackedWidget.setCurrentIndex(i)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.display(1)


def run_application(experiment):
    app = QApplication([])
    ex = Application()
    app.exec_()