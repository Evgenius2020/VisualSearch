from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from Configuration import Configuration
from Frontend.PagesWidget import PagesWidget


class Application(PagesWidget):
    def __init__(self, experiment):
        super().__init__()
        self.__experiment__ = experiment

    def __on_trial_start__(self):
        self.__current_trial__ = self.__experiment__.get_current_trial()
        if self.__current_trial__ is None:
            self.change_page(self.EXPERIMENT_END_PAGE)
            return
        self.set_trial_bars_to_display(self.__current_trial__.bars_to_display)
        self.change_page(self.FIXATION_PAGE)
        QTimer.singleShot(Configuration.FIXATION_DURATION, lambda: self.change_page(self.TRIAL_PAGE))

    def __on_trial_response__(self, answer_is_correct):
        if answer_is_correct:
            self.change_page(self.FEEDBACK_CORRECT_PAGE)
        else:
            self.change_page(self.FEEDBACK_INCORRECT_PAGE)
        self.__experiment__.go_next_trial()
        QTimer.singleShot(Configuration.FEEDBACK_DURATION, self.__on_trial_start__)

    def keyPressEvent(self, event):
        # print(event.text())
        if self.page == self.INTRO_PAGE:
            if event.key() == QtCore.Qt.Key_Space:
                self.__on_trial_start__()
        elif self.page == self.TRIAL_PAGE:
            answer = None
            if event.text().upper() == Configuration.KEYBOARD_KEY_FOR_PRESENTED:
                answer = Configuration.KEYBOARD_KEY_FOR_PRESENTED
            elif event.text().upper() == Configuration.KEYBOARD_KEY_FOR_ABSENT:
                answer = Configuration.KEYBOARD_KEY_FOR_ABSENT
            if answer is not None:
                answer_is_correct = \
                    self.__current_trial__.target_is_presented and answer == Configuration.KEYBOARD_KEY_FOR_PRESENTED or \
                    not self.__current_trial__.target_is_presented and answer == Configuration.KEYBOARD_KEY_FOR_ABSENT
                self.__on_trial_response__(answer_is_correct)


def run_application(experiment):
    qa = QApplication([])
    application = Application(experiment)
    qa.exec_()
