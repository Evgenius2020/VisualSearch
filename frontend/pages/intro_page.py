from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from backend.trial import Trial
import configuration
from frontend.pages.trial_page import TrialPage


class IntroPage(QWidget):
    """
    Page with experiment description, key bindings and present/absent target trials examples.

    :param keyboard_key_for_presented: Keyboard key that associated with 'target presented' response.
    :param keyboard_key_for_absent: Keyboard key that associated with 'target absent' response.
    """
    class ExamplePage(QWidget):
        """
        Page with trial page and text description.

        :param trial_page: Trial page to display.
        :param text: Description text to display under 'trial_page'.
        """
        def __init__(self,
                     trial_page: TrialPage,
                     text: str):
            super().__init__()
            layout = QVBoxLayout(self)
            layout.addWidget(trial_page)
            layout.addWidget(QLabel(text))
            trial_page.setMinimumHeight(500)
            self.setLayout(layout)

    def __init__(self,
                 keyboard_key_for_presented: str,
                 keyboard_key_for_absent: str):
        super().__init__()
        layout = QVBoxLayout(self)

        label = QLabel(configuration.INTRO_TEXT)
        layout.addWidget(label)

        presented_trial_page = TrialPage()
        presented_trial_page.set_bars_to_display(Trial(12, True, True).bars_to_display)
        presented_example_page = self.ExamplePage(presented_trial_page,
                                                  configuration.KEY_BINDINGS_PRESENTED_FORMAT_STRING %
                                                  keyboard_key_for_presented)

        absent_trial_page = TrialPage()
        absent_trial_page.set_bars_to_display(Trial(16, False, False).bars_to_display)
        absent_example_page = self.ExamplePage(absent_trial_page,
                                               configuration.KEY_BINDINGS_ABSENT_FORMAT_STRING %
                                               keyboard_key_for_absent)

        examples = QWidget()
        examples_layout = QHBoxLayout(self)
        examples_layout.addWidget(presented_example_page)
        examples_layout.addWidget(absent_example_page)
        examples.setLayout(examples_layout)
        layout.addWidget(examples)

        label = QLabel(configuration.INTRO_END_TEXT)
        layout.addWidget(label)

        self.setLayout(layout)
