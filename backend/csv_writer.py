from typing import TextIO

from backend.experiment import Experiment


class CsvWriter:
    """
    Special csv writer for logging trial results.

    :param csv_stream: The text stream in which the trial results will be written.

    :ivar __csv_stream__: The text stream in which the trial results will be written.
    """
    __csv_stream__: TextIO

    def __init__(self,
                 csv_stream: TextIO):
        self.__csv_stream__ = csv_stream
        # Write header.
        self.__write_row__(["subject_name",
                            "presented_key",
                            "absent_key",
                            "block",
                            "condition",
                            "trial",
                            "targets",
                            "target_presented",
                            "target_vertical",
                            "response_correct",
                            "response_time"])

    def __write_row__(self,
                      row: list) -> None:
        """
        Write to stream row of values.

        :param row: List of values.
        """
        self.__csv_stream__.write(",".join([str(el) for el in row]) + "\n")
        self.__csv_stream__.flush()

    def write_trial_result(self,
                           experiment: Experiment,
                           response_correct: bool,
                           response_time: int) -> None:
        """
        Write to stream trial result.

        :param experiment: Current experiment (to obtain full trial info).
        :param response_correct: Correctness of subject response.
        :param response_time: Time of subject response in milliseconds.

        :raises: :class:`ValueError`: Experiment is finished. No trial to apply result.
        """
        curr_trial = experiment.get_current_trial()
        if curr_trial is None:
            raise ValueError("Experiment is finished. No trial to apply result.")
        curr_block = experiment.blocks[experiment.current_block_id]
        data = [experiment.subject_name,
                experiment.keyboard_key_for_presented,
                experiment.keyboard_key_for_absent,
                experiment.current_block_id + 1,
                curr_block.condition_name,
                experiment.current_trial_id + 1,
                curr_trial.targets_number,
                1 if curr_trial.target_is_presented else 0,
                1 if curr_trial.target_orientation_is_vertical else 0,
                1 if response_correct else 0,
                response_time]
        self.__write_row__(data)
