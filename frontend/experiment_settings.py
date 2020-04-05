from typing import TextIO

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QCheckBox, QMessageBox

import configuration


class ExperimentSettings(QDialog):
    """
    Dialog with experiment settings. User can set here 'subject_name', 'csv_file' and enable fast mode.

    :ivar subject_name: Name of the subject.
    :ivar csv_file: Csv file for experiment results logging.
    :ivar fast_mode_enabled: 'True' if fast mode enabled, 'False' otherwise.
    :ivar __csv_file_path__: Path to csv file.
    """
    subject_name: str
    csv_file: TextIO
    fast_mode_enabled: bool
    __csv_file_path__: str

    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisualSearch")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setFixedSize(300, 180)
        self.subject_name = configuration.DEFAULT_SUBJECT_NAME
        self.csv_file = None
        self.fast_mode_enabled = False
        self.__csv_file_path__ = ""

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Subject name:"))
        subject_name_edit = QLineEdit(self.subject_name)
        layout.addWidget(subject_name_edit)
        csv_filename_label = QLabel()
        layout.addWidget(csv_filename_label)
        select_file_button = QPushButton("Change filename")
        layout.addWidget(select_file_button)
        layout.addStretch(10)
        fast_mode_check_box = QCheckBox("Fast mode (%d blocks, %d trials each; no practice)" %
                                        (configuration.FAST_MODE_BLOCKS_PER_CONDITION * 4,
                                         configuration.FAST_MODE_TRIALS_PER_BLOCK))
        layout.addWidget(fast_mode_check_box)
        start_button = QPushButton("Start experiment")
        layout.addWidget(start_button)
        self.setLayout(layout)

        def csv_filename_label_set_text(csv_filename: str) -> None:
            """
            Put new csv filename in 'csv_filename_label' (shorten if needed).

            :param csv_filename: Csv filename.
            """
            if len(csv_filename) > 25:
                csv_filename = "..." + csv_filename[-25:]
            csv_filename_label.setText("Csv file: '%s'" % csv_filename)

        def subject_name_edit_text_changed(new_subject_name: str) -> None:
            """
            Save new name and set it as csv filename.

            :param new_subject_name: New subject name.
            """
            self.subject_name = new_subject_name
            csv_filename = new_subject_name + configuration.CSV_FILE_EXTENSION
            self.__csv_file_path__ = csv_filename
            csv_filename_label_set_text(csv_filename)

        def select_file_button_clicked() -> None:
            """
            Show csv file selection dialog.
            On file selected, saves path and show it's name in 'csv_filename_label'.
            """
            csv_filename = QFileDialog.getSaveFileName(None,
                                                       "Select csv file",
                                                       self.subject_name,
                                                       "*" + configuration.CSV_FILE_EXTENSION)[0]
            # 'Cancel' handling.
            if csv_filename == "":
                return

            self.__csv_file_path__ = csv_filename
            csv_filename_label_set_text(csv_filename)

        def start_button_clicked() -> None:
            """
            On 'start_button' click, open csv file and close dialog.
            If file open is failed, show message about it.
            """
            try:
                self.csv_file = open(self.__csv_file_path__, "w")
            except OSError:
                error_message_box = QMessageBox(parent=self)
                error_message_box.icon = QMessageBox.Critical
                error_message_box.setWindowTitle("File open failed")
                error_message_box.setText(
                    ("Failed to open csv file '%s'\n" % self.__csv_file_path__) +
                    "Check that filename not contains forbidden symbols (e.g. '*', '|', '?') "
                    "and this program have permissions to write to this file.")
                error_message_box.show()
                return
            self.fast_mode_enabled = fast_mode_check_box.isChecked()
            self.close()

        subject_name_edit.textChanged[str].connect(subject_name_edit_text_changed)
        subject_name_edit.setText(configuration.DEFAULT_SUBJECT_NAME)
        subject_name_edit_text_changed(subject_name_edit.text())
        select_file_button.clicked.connect(select_file_button_clicked)
        start_button.clicked.connect(start_button_clicked)
