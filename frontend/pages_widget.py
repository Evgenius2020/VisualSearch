from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStackedWidget, QFormLayout

from backend.trial import Bar
import configuration
from frontend.pages.intro_page import IntroPage
from frontend.pages.one_string_page import OneStringPage
from frontend.pages.trial_page import TrialPage


class PagesWidget(QWidget):
    """
    Contains all pages of experiment, shows them and can switch page to display.

    :param keyboard_key_for_presented: Keyboard key that associated with 'target presented' response.
    :param keyboard_key_for_absent: Keyboard key that associated with 'target absent' response.

    :ivar intro_page_id: Id of 'Intro' page.
    :ivar fixation_page_id: Id of 'Fixation' page.
    :ivar trial_page_id: Id of 'Trial' page.
    :ivar feedback_correct_page_id: Id of 'Feedback correct' page.
    :ivar feedback_incorrect_page_id: Id of 'Feedback incorrect' page.
    :ivar block_end_rest_page_id: Id of 'Block end rest' page.
    :ivar experiment_end_page_id: Id of 'Experiment end' page.

    :ivar page_id: Current page id.
    :ivar __trial_page__: TrialPage instance.
    :ivar __pages__: Widget with all pages.
    """
    intro_page_id: int
    fixation_page_id: int
    trial_page_id: int
    feedback_correct_page_id: int
    feedback_incorrect_page_id: int
    experiment_end_page_id: int

    page_id: int
    __trial_page__: TrialPage
    __pages__: QStackedWidget

    def __init__(self,
                 keyboard_key_for_presented: str,
                 keyboard_key_for_absent: str):
        super().__init__()

        trial_page = TrialPage()
        pages = QStackedWidget(self)
        pages.addWidget(IntroPage(keyboard_key_for_presented, keyboard_key_for_absent))  # Intro
        pages.addWidget(OneStringPage("+"))  # Fixation
        pages.addWidget(trial_page)  # Trial
        pages.addWidget(OneStringPage(configuration.FEEDBACK_CORRECT_TEXT, "green"))  # Feedback correct
        pages.addWidget(OneStringPage(configuration.FEEDBACK_INCORRECT_TEXT, "red"))  # Feedback incorrect
        pages.addWidget(OneStringPage(configuration.BLOCK_END_REST_TEXT))  # Block end rest
        pages.addWidget(OneStringPage(configuration.EXPERIMENT_END_TEXT))  # Experiment end

        self.setStyleSheet(
            "QLabel { color : white; font-size: 18px; qproperty-alignment: AlignCenter;} "
            "Application {background-color: black;}")
        self.setCursor(Qt.BlankCursor)
        layout = QFormLayout()
        layout.addWidget(pages)
        self.setLayout(layout)
        self.showFullScreen()

        self.intro_page_id = 0
        self.fixation_page_id = 1
        self.trial_page_id = 2
        self.feedback_correct_page_id = 3
        self.feedback_incorrect_page_id = 4
        self.block_end_rest_page_id = 5
        self.experiment_end_page_id = 6

        self.page_id = self.intro_page_id
        self.__trial_page__ = trial_page
        self.__pages__ = pages

        self.change_page(self.intro_page_id)

    def change_page(self,
                    page_id: int) -> None:
        """
        Change current page to show.

        :param page_id: Page id.
        """
        self.page_id = page_id
        self.__pages__.setCurrentIndex(page_id)

    def set_trial_bars_to_display(self,
                                  bars: List[Bar]) -> None:
        """
        Change trial bars to display at 'TrialPage'.

        :param bars: List of bars to display.
        """
        self.__trial_page__.set_bars_to_display(bars)
