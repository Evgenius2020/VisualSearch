from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStackedWidget, QFormLayout

from Configuration import Configuration
from Frontend.Pages.IntroPage import IntroPage
from Frontend.Pages.OneStringPage import OneStringPage
from Frontend.Pages.TrialPage import TrialPage


class PagesWidget(QWidget):
    INTRO_PAGE = 0
    FIXATION_PAGE = 1
    TRIAL_PAGE = 2
    FEEDBACK_CORRECT_PAGE = 3
    FEEDBACK_INCORRECT_PAGE = 4
    EXPERIMENT_END_PAGE = 5

    def __init__(self):
        super().__init__()

        trial_page = TrialPage()
        pages = QStackedWidget(self)
        pages.addWidget(IntroPage())
        pages.addWidget(OneStringPage("+"))  # fixation
        pages.addWidget(trial_page)
        pages.addWidget(OneStringPage(Configuration.FEEDBACK_CORRECT_TEXT, "green"))  # feedback_correct
        pages.addWidget(OneStringPage(Configuration.FEEDBACK_INCORRECT_TEXT, "red"))  # feedback_incorrect
        pages.addWidget(OneStringPage(Configuration.EXPERIMENT_END_TEXT))  # experiment_end

        self.__trial_page__ = trial_page
        self.__pages__ = pages
        self.setStyleSheet(
            "QLabel { color : white; font-size: 18px; qproperty-alignment: AlignCenter;} "
            "Application {background-color: black;}")
        self.setCursor(Qt.BlankCursor)
        layout = QFormLayout()
        layout.addWidget(pages)
        self.setLayout(layout)
        self.page = self.INTRO_PAGE
        self.change_page(self.INTRO_PAGE)
        self.showFullScreen()

    def change_page(self, page):
        self.page = page
        self.__pages__.setCurrentIndex(page)

    def set_trial_bars_to_display(self, bars):
        self.__trial_page__.set_bars_to_display(bars)