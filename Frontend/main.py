import sys
from random import random

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import *


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")
        self.ww = self.size().width()
        self.wh = self.size().height()
        self.setGeometry(0, 0, self.ww, self.wh)

        # square stimulus area
        self.grid_margin = (self.ww // 50, self.ww // 50)
        self.grid_start_coord = ((self.ww - self.wh) // 2 + self.grid_margin[0], self.grid_margin[1])
        self.grid_size = (self.wh - self.grid_margin[0] * 2, self.wh - self.grid_margin[1] * 2)
        self.grid_bars_ids = [[0, 1, 4, 5], [2, 3, 6, 7], [8, 9, 12, 13], [10, 11, 14, 15]]
        self.bar_box_size = (self.grid_size[0] // 4, self.grid_size[1] // 4)
        self.bar_box_padding = (self.bar_box_size[0] // 20, self.bar_box_size[1] // 20)
        self.bar_vertical_size = (self.bar_box_size[0] // 10 * 2, self.bar_box_size[1] // 10 * 7)
        self.bar_vertical_shift_size = (self.bar_box_size[0] - self.bar_vertical_size[0] - 2 * self.bar_box_padding[0],
                                        self.bar_box_size[1] - self.bar_vertical_size[1] - 2 * self.bar_box_padding[1])
        self.bar_horizontal_size = (self.bar_vertical_size[1], self.bar_vertical_size[0])
        self.bar_horizontal_shift_size = (
            self.bar_box_size[0] - self.bar_horizontal_size[0] - 2 * self.bar_box_padding[0],
            self.bar_box_size[1] - self.bar_horizontal_size[1] - 2 * self.bar_box_padding[1])

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        for grid_sector in range(4):
            for grid_square in range(4):
                if random() > 0.5:
                    qp.setBrush(QColor(255, 0, 0))
                else:
                    qp.setBrush(QColor(0, 255, 0))
                bar_x, bar_y, bar_width, bar_height = self.generate_bar_rect(grid_sector, grid_square, random() > 0.5)
                qp.drawRect(bar_x, bar_y, bar_width, bar_height)
        qp.end()

    def generate_bar_rect(self, square, sector, vertical):
        grid_id = self.grid_bars_ids[square][sector]
        x = self.grid_start_coord[0] + (grid_id % 4) * self.bar_box_size[0] + self.bar_box_padding[0]
        y = self.grid_start_coord[1] + (grid_id // 4) * self.bar_box_size[1] + self.bar_box_padding[1]
        if vertical:
            x += int(self.bar_vertical_shift_size[0] * random())
            y += int(self.bar_vertical_shift_size[1] * random())
            return x, y, self.bar_vertical_size[0], self.bar_vertical_size[1]
        else:
            x += int(self.bar_horizontal_shift_size[0] * random())
            y += int(self.bar_horizontal_shift_size[1] * random())
            return x, y, self.bar_horizontal_size[0], self.bar_horizontal_size[1]

    def keyPressEvent(self, ev):
        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
