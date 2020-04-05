from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication

from backend.experiment import Experiment
from backend.csv_writer import CsvWriter
import configuration
from frontend.experiment_settings import ExperimentSettings
from frontend.pages_widget import PagesWidget


class Application(PagesWidget):
    """
    Main entity. Contains all pages, Experiment and CsvWriter instances.
    Interaction events described here.

    :param experiment: Experiment.
    :param csv_writer: CsvWriter for experiment progress logging.

    :ivar __experiment__: Experiment.
    :ivar __csv_writer__: CsvWriter for experiment progress logging.
    :ivar __trial_start_timestamp__: Timestamp of last trial start. Used to measure response time.
    :ivar __practice_complete_handled__: Boolean flag whether practice complete event is handled.
    """
    __experiment__: Experiment
    __csv_writer__: CsvWriter
    __trial_start_timestamp__: datetime
    __practice_complete_handled__: bool

    def __init__(self,
                 experiment: Experiment,
                 csv_writer: CsvWriter):
        super().__init__(experiment.keyboard_key_for_presented,
                         experiment.keyboard_key_for_absent)
        self.__experiment__ = experiment
        self.__csv_writer__ = csv_writer
        self.__trial_start_timestamp__ = None
        self.__practice_complete_handled__ = False if configuration.PRACTICE_TRIALS_NUMBER > 0 else True

    def __on_trial_start__(self) -> None:
        """
        On trial start, change displayed bars and run fixation.
        If experiment is passed, go 'Experiment end' page.
        If practice is passed, go 'Practice end' page.
        If trials block passed (not, go 'Block end rest' page.
        """
        if self.__experiment__.is_experiment_complete:
            self.change_page(self.experiment_end_page_id)
            return

        if not self.__practice_complete_handled__ and \
                self.__experiment__.is_practice_complete:
            self.__practice_complete_handled__ = True
            self.change_page(self.practice_end_page_id)
            return

        if self.__experiment__.is_block_complete:
            self.__experiment__.is_block_complete = False
            self.change_page(self.block_end_rest_page_id)
            QTimer.singleShot(configuration.BLOCK_END_REST_DURATION, self.__on_trial_start__)
            return

        self.__current_trial__ = self.__experiment__.get_current_trial()
        self.set_trial_bars_to_display(self.__current_trial__.bars_to_display)
        self.change_page(self.fixation_page_id)
        QTimer.singleShot(configuration.FIXATION_DURATION, self.__on_fixation_end__)

    def __on_fixation_end__(self) -> None:
        """
        On fixation end, show bars and make trial start timestamp.
        """
        self.change_page(self.trial_page_id)
        self.__trial_start_timestamp__ = datetime.now()

    def __on_trial_response__(self,
                              response_correct: bool,
                              response_time: int) -> None:
        """
        On trial response (when subject pressed the key), log trial results and go to next trial.

        :param response_correct: Correctness of subject response.
        :param response_time: Time of subject response in milliseconds.
        """
        if response_correct:
            self.change_page(self.feedback_correct_page_id)
        else:
            self.change_page(self.feedback_incorrect_page_id)

        # No logging at practice trials.
        if self.__experiment__.is_practice_complete:
            self.__csv_writer__.write_trial_result(self.__experiment__,
                                                   response_correct,
                                                   response_time)
        self.__experiment__.go_next_trial()
        QTimer.singleShot(configuration.FEEDBACK_DURATION,
                          self.__on_trial_start__)

    def keyPressEvent(self,
                      e: QKeyEvent) -> None:
        """
        keyPressEvent handling depending on current page.

        :param e: QKeyEvent.
        """
        if self.page_id == self.intro_page_id:
            # At 'Intro' page, subject can press SPACE to continue.
            if e.key() == QtCore.Qt.Key_Space:
                self.__on_trial_start__()
        elif self.page_id == self.trial_page_id:
            # At trial page, subject can press 'keyboard_key_for_presented' or 'keyboard_key_for_absent' to pass trial.
            answer = e.text().upper()
            if answer in [self.__experiment__.keyboard_key_for_presented,
                          self.__experiment__.keyboard_key_for_absent]:
                time_delta = int((datetime.now() - self.__trial_start_timestamp__).total_seconds() * 1000)

                response_correct = \
                    self.__current_trial__.target_is_presented and \
                    answer == self.__experiment__.keyboard_key_for_presented or \
                    not self.__current_trial__.target_is_presented and \
                    answer == self.__experiment__.keyboard_key_for_absent

                self.__on_trial_response__(response_correct, time_delta)
        elif self.page_id == self.practice_end_page_id:
            # At 'Practice end' page, subject can press SPACE to start experiment trials.
            if e.key() == QtCore.Qt.Key_Space:
                self.__on_trial_start__()
        elif self.page_id == self.experiment_end_page_id:
            # At 'Experiment end' page, subject can press SPACE to close application.
            if e.key() == QtCore.Qt.Key_Space:
                self.close()


def run_application() -> None:
    """
    Run application.
    1) ExperimentSettings dialog will be shown.
    2) If fast mode is enabled, changes experiment settings.
    3) Creates Experiment and CsvWriter instances and runs experiment.
    """
    qa = QApplication([])
    experiment_settings = ExperimentSettings()
    experiment_settings.exec_()
    if experiment_settings.csv_file is None:
        return
    if experiment_settings.fast_mode_enabled:
        configuration.CONJUNCTION_CONDITION_BLOCKS_NUMBER = configuration.FAST_MODE_BLOCKS_PER_CONDITION
        configuration.SWITCH_CONDITION_BLOCKS_NUMBER = configuration.FAST_MODE_BLOCKS_PER_CONDITION
        configuration.STREAK_CONDITION_BLOCKS_NUMBER = configuration.FAST_MODE_BLOCKS_PER_CONDITION
        configuration.RANDOM_CONDITION_BLOCKS_NUMBER = configuration.FAST_MODE_BLOCKS_PER_CONDITION
        configuration.TRIALS_PER_BLOCK = configuration.FAST_MODE_TRIALS_PER_BLOCK
        # No practice in fast mode.
        configuration.INTRO_END_TEXT = configuration.INTRO_END_FAST_MODE_TEXT
        configuration.PRACTICE_TRIALS_NUMBER = 0
    application = Application(Experiment(experiment_settings.subject_name),
                              CsvWriter(experiment_settings.csv_file))
    qa.exec_()
