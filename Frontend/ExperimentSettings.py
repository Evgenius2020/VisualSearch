from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QCheckBox

from Configuration import Configuration


class ExperimentSettings(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisualSearch")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setFixedSize(300, 180)
        self.subject_name = Configuration.DEFAULT_SUBJECT_NAME
        self.protocol_filename = ""
        self.protocol_file = None
        self.fast_mode_enabled = False

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Subject name:"))
        subject_name_edit = QLineEdit(self.subject_name)
        layout.addWidget(subject_name_edit)
        protocol_filename_label = QLabel()
        layout.addWidget(protocol_filename_label)
        select_file_button = QPushButton("Change filename")
        layout.addWidget(select_file_button)
        layout.addStretch(10)
        fast_mode_check_box = QCheckBox("Fast mode (%d blocks, %d trials each)" %
                                        (Configuration.FAST_MODE_BLOCK_PER_CONDITION * 4,
                                         Configuration.FAST_MODE_TRIALS_PER_BLOCK))
        layout.addWidget(fast_mode_check_box)
        start_button = QPushButton("Start experiment")
        layout.addWidget(start_button)
        self.setLayout(layout)

        def subject_name_edit_text_changed(text):
            pf = text + Configuration.PROTOCOL_FILE_EXTENSION
            self.protocol_filename = pf
            protocol_filename_label.setText("Protocol file: '%s'" % pf)

        def select_file_button_clicked():
            pf = QFileDialog.getSaveFileName(None, "Select protocol file", self.subject_name, "*.csv")[0]
            self.protocol_filename = pf
            if len(pf) > 35:
                pf = "..." + pf[-35:]
            protocol_filename_label.setText("Protocol file: '%s'" % pf)

        def start_button_clicked():
            self.protocol_file = open(self.protocol_filename, "w")
            self.fast_mode_enabled = fast_mode_check_box.isChecked()
            self.close()

        subject_name_edit.textChanged[str].connect(subject_name_edit_text_changed)
        subject_name_edit.setText(Configuration.DEFAULT_SUBJECT_NAME)
        subject_name_edit_text_changed(subject_name_edit.text())
        select_file_button.clicked.connect(select_file_button_clicked)
        start_button.clicked.connect(start_button_clicked)
