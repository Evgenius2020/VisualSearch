from random import random

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import *


class Bar:
    def __init__(self, grid_sector_id, bar_box_id, color_is_red, orientation_is_vertical):
        self.grid_sector_id = grid_sector_id
        self.bar_box_id = bar_box_id
        self.color_is_red = color_is_red
        self.orientation_is_vertical = orientation_is_vertical
        self.shift = (random(), random())


class Trial(QWidget):
    class RenderOptions:
        grid_start_coord = None
        bar_box_size = None
        bar_box_padding = None
        bar_vertical_size = None
        bar_vertical_shift_size = None
        bar_horizontal_size = None
        bar_horizontal_shift_size = None

    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")

        # 0  1  2  3
        # 4  5  6  7
        # 8  9  10 11
        # 12 13 14 15
        self.__grid_bars_ids__ = [[0, 1, 4, 5], [2, 3, 6, 7], [8, 9, 12, 13], [10, 11, 14, 15]]
        self.__bars_to_display__ = []

        # square stimulus area
        ww = self.size().width()
        wh = self.size().height()
        self.setGeometry(0, 0, ww, wh)
        ro = self.RenderOptions()
        grid_margin = (ww // 50, ww // 50)
        grid_size = (wh - grid_margin[0] * 2, wh - grid_margin[1] * 2)
        ro.grid_start_coord = ((ww - wh) // 2 + grid_margin[0], grid_margin[1])
        ro.bar_box_size = (grid_size[0] // 4, grid_size[1] // 4)
        ro.bar_box_padding = (ro.bar_box_size[0] // 20, ro.bar_box_size[1] // 20)
        ro.bar_vertical_size = (ro.bar_box_size[0] // 10 * 2, ro.bar_box_size[1] // 10 * 7)
        ro.bar_vertical_shift_size = (ro.bar_box_size[0] - ro.bar_vertical_size[0] - 2 * ro.bar_box_padding[0],
                                      ro.bar_box_size[1] - ro.bar_vertical_size[1] - 2 * ro.bar_box_padding[1])
        ro.bar_horizontal_size = (ro.bar_vertical_size[1], ro.bar_vertical_size[0])
        ro.bar_horizontal_shift_size = (
            ro.bar_box_size[0] - ro.bar_horizontal_size[0] - 2 * ro.bar_box_padding[0],
            ro.bar_box_size[1] - ro.bar_horizontal_size[1] - 2 * ro.bar_box_padding[1])
        self.__render_options__ = ro

    def __generate_bar_rect__(self, bar):
        ro = self.__render_options__
        grid_id = self.__grid_bars_ids__[bar.grid_sector_id][bar.bar_box_id]
        x = ro.grid_start_coord[0] + (grid_id % 4) * ro.bar_box_size[0] + ro.bar_box_padding[0]
        y = ro.grid_start_coord[1] + (grid_id // 4) * ro.bar_box_size[1] + ro.bar_box_padding[1]
        if bar.orientation_is_vertical:
            x += int(ro.bar_vertical_shift_size[0] * bar.shift[0])
            y += int(ro.bar_vertical_shift_size[1] * bar.shift[1])
            return x, y, ro.bar_vertical_size[0], ro.bar_vertical_size[1]
        else:
            x += int(ro.bar_horizontal_shift_size[0] * bar.shift[0])
            y += int(ro.bar_horizontal_shift_size[1] * bar.shift[1])
            return x, y, ro.bar_horizontal_size[0], ro.bar_horizontal_size[1]

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        for bar in self.__bars_to_display__:
            if bar.color_is_red:
                qp.setBrush(QColor(255, 0, 0))
            else:
                qp.setBrush(QColor(0, 255, 0))
            bar_x, bar_y, bar_width, bar_height = self.__generate_bar_rect__(bar)
            qp.drawRect(bar_x, bar_y, bar_width, bar_height)
        qp.end()

    def set_bars_to_display(self, bars_to_display):
        self.__bars_to_display__ = bars_to_display
        self.repaint()


if __name__ == '__main__':
    app = QApplication([])
    ex = Trial()
    ex.set_bars_to_display([Bar(0, 0, False, False), Bar(3, 3, True, True)])
    app.exec_()
