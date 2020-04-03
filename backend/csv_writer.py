from typing import TextIO, List

from backend.experiment import Experiment


class CsvWriter:
    def __init__(self,
                 csv_file: TextIO):
        self.__csv_file__ = csv_file
        self.write_row(["subject_name",
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

    def write_row(self,
                  row: List):
        self.__csv_file__.write(",".join([str(el) for el in row]) + "\n")
        self.__csv_file__.flush()

    def write_trial_result(self,
                           experiment: Experiment,
                           response_correct: bool,
                           response_time: int) -> None:
        curr_trial = experiment.get_current_trial()
        if curr_trial is None:
            raise ValueError("Experiment is finished")
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
        self.write_row(data)
