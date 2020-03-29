from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from Backend.Trial import Trial
from Configuration import Configuration
from Frontend.Pages.TrialPage import TrialPage


class IntroPage(QWidget):
    class ExamplePage(QWidget):
        def __init__(self, trial_page, text):
            super().__init__()
            layout = QVBoxLayout(self)
            label = QLabel(text)
            layout.addWidget(trial_page)
            layout.addWidget(label)
            trial_page.setMinimumHeight(500)
            self.setLayout(layout)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("QLabel { font-size: 18px; qproperty-alignment: AlignCenter;}")
        layout = QVBoxLayout(self)

        label = QLabel(Configuration.INTRO_TEXT)
        layout.addWidget(label)

        presented_trial_page = TrialPage()
        presented_trial_page.set_bars_to_display(Trial(12, True, True).generate_bars_to_display())
        presented_example_page = self.ExamplePage(presented_trial_page,
                                                  Configuration.KEY_BINDINGS_PRESENTED_FORMAT_STRING %
                                                  Configuration.KEYBOARD_KEY_FOR_PRESENTED)

        absent_trial_page = TrialPage()
        absent_trial_page.set_bars_to_display(Trial(16, False, False).generate_bars_to_display())
        absent_example_page = self.ExamplePage(absent_trial_page,
                                               Configuration.KEY_BINDINGS_ABSENT_FORMAT_STRING %
                                               Configuration.KEYBOARD_KEY_FOR_ABSENT)

        examples = QWidget()
        examples_layout = QHBoxLayout(self)
        examples_layout.addWidget(presented_example_page)
        examples_layout.addWidget(absent_example_page)
        examples.setLayout(examples_layout)
        layout.addWidget(examples)

        label = QLabel(Configuration.INTRO_START_EXPERIMENT_TEXT)
        layout.addWidget(label)

        self.setLayout(layout)
