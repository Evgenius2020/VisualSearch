from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class OneStringPage(QWidget):
    """
    Page with one text string at center.

    :param string: Text string to display.
    :param string_color: Color of displayed text.
    """
    def __init__(self,
                 string: str,
                 string_color="white"):
        super().__init__()
        layout = QHBoxLayout()
        self.setStyleSheet("QLabel { font-size: 30px; font-weight: bold; color: %s;}" % string_color)
        layout.addWidget(QLabel(string))
        self.setLayout(layout)
