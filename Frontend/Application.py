from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStackedWidget, QApplication, QFormLayout

from Backend.Bar import Bar
from Frontend.Pages.IntroPage import IntroPage
from Frontend.Pages.TrialPage import TrialPage


class Application(QWidget):
    def __init__(self):
        super().__init__()
        # self.showFullScreen()
        pages = QStackedWidget(self)
        pages.addWidget(IntroPage())
        trial_page = TrialPage()
        trial_page.set_bars_to_display([Bar(0, 0, False, False), Bar(3, 3, True, True)])
        pages.addWidget(trial_page)

        self.__trial_page__ = trial_page
        self.__pages__ = pages
        self.setStyleSheet("QLabel { color : white; } Application {background-color: black;}")
        self.setCursor(Qt.BlankCursor)
        layout = QFormLayout()
        layout.addWidget(pages)
        self.setLayout(layout)
        self.show()

    def __change_page__(self, i):
        self.__pages__.setCurrentIndex(i)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.__change_page__(1)


def run_application(experiment):
    app = QApplication([])
    ex = Application()
    app.exec_()
