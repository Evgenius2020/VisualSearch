from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from backend.experiment import Experiment
from configuration import Configuration
from frontend.experiment_settings import ExperimentSettings
from frontend.pages_widget import PagesWidget
from frontend.protocol_writer import ProtocolWriter


class Application(PagesWidget):
    def __init__(self, experiment, protocol_writer):
        super().__init__(experiment.keyboard_key_for_presented, experiment.keyboard_key_for_absent)
        self.__experiment__ = experiment
        self.__protocol_writer__ = protocol_writer

    def __on_trial_start__(self):
        self.__current_trial__ = self.__experiment__.get_current_trial()
        if self.__current_trial__ is None:
            self.change_page(self.EXPERIMENT_END_PAGE)
            return

        self.set_trial_bars_to_display(self.__current_trial__.bars_to_display)
        self.change_page(self.FIXATION_PAGE)
        QTimer.singleShot(Configuration.FIXATION_DURATION, self.__on_fixation_end__)

    def __on_fixation_end__(self):
        self.change_page(self.TRIAL_PAGE)
        self.__trial_start_timestamp__ = datetime.now()

    def __on_trial_response__(self, response_correct):
        time_delta = int((datetime.now() - self.__trial_start_timestamp__).total_seconds() * 1000)
        if response_correct:
            self.change_page(self.FEEDBACK_CORRECT_PAGE)
        else:
            self.change_page(self.FEEDBACK_INCORRECT_PAGE)
        self.__protocol_writer__.append_trial_result(self.__experiment__, response_correct, time_delta)
        self.__experiment__.go_next_trial()
        QTimer.singleShot(Configuration.FEEDBACK_DURATION, self.__on_trial_start__)

    def keyPressEvent(self, event):
        if self.page == self.INTRO_PAGE:
            if event.key() == QtCore.Qt.Key_Space:
                self.__on_trial_start__()
        elif self.page == self.TRIAL_PAGE:
            answer = event.text().upper()
            if answer in [self.__experiment__.keyboard_key_for_presented,
                          self.__experiment__.keyboard_key_for_absent]:
                response_correct = self.__current_trial__.target_is_presented and \
                                   answer == self.__experiment__.keyboard_key_for_presented or \
                                   not self.__current_trial__.target_is_presented and \
                                   answer == self.__experiment__.keyboard_key_for_absent
                self.__on_trial_response__(response_correct)
        elif self.page == self.EXPERIMENT_END_PAGE:
            if event.key() == QtCore.Qt.Key_Space:
                self.close()


def run_application():
    qa = QApplication([])
    my_dialog = ExperimentSettings()
    my_dialog.exec_()
    if my_dialog.protocol_file is None:
        return
    if my_dialog.fast_mode_enabled:
        Configuration.CONJUNCTION_CONDITION_BLOCKS_NUMBER = Configuration.FAST_MODE_BLOCKS_PER_CONDITION
        Configuration.SWITCH_CONDITION_BLOCKS_NUMBER = Configuration.FAST_MODE_BLOCKS_PER_CONDITION
        Configuration.STREAK_CONDITION_BLOCKS_NUMBER = Configuration.FAST_MODE_BLOCKS_PER_CONDITION
        Configuration.RANDOM_CONDITION_BLOCKS_NUMBER = Configuration.FAST_MODE_BLOCKS_PER_CONDITION
        Configuration.TRIALS_PER_BLOCK = Configuration.FAST_MODE_TRIALS_PER_BLOCK
    application = Application(Experiment(my_dialog.subject_name), ProtocolWriter(my_dialog.protocol_file))
    qa.exec_()
