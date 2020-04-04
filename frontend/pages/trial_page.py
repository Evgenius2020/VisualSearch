from typing import List, Tuple

from PyQt5.QtGui import QPainter, QColor, QResizeEvent, QPaintEvent
from PyQt5.QtWidgets import *

from backend.trial import Bar


class RenderOptions:
    """
    Render options for bars displaying. Render options depends on page size and must be recalculated on page resize.

    :ivar grid_start_coord: (x; y) coordinates of grid left-top point.
    :ivar bar_box_size: (x; y) size of bar box.
    :ivar bar_box_padding: (x; y) size of bar box padding (left-top-right-bottom).
    :ivar bar_vertical_size: (x; y) size of vertical bar.
    :ivar bar_vertical_shift_size: (x; y) size of possible shift of vertical bar.
    :ivar bar_horizontal_size: (x; y) size of horizontal bar.
    :ivar bar_horizontal_shift_size: (x; y) size of possible shift of horizontal bar.
    """
    grid_start_coord: Tuple[int, int]
    bar_box_size: Tuple[int, int]
    bar_box_padding: Tuple[int, int]
    bar_vertical_size: Tuple[int, int]
    bar_vertical_shift_size: Tuple[int, int]
    bar_horizontal_size: Tuple[int, int]
    bar_horizontal_shift_size: Tuple[int, int]


class TrialPage(QWidget):
    """
    Page for displaying bars of trials. Bars are displayed in square area (grid) in center of page.

    :ivar __grid_bars_ids__: Mapping from bar (grid_sector_id; bar_box_id) coordinates to (grid_bar_id) coordinate.
    :ivar __bars_to_display__: Bars to display.
    :ivar __render_options__: Render options.
    """
    __grid_bars_ids__: List[List[int]]
    __bars_to_display__: List[Bar]
    __render_options__: RenderOptions

    def __init__(self):
        super().__init__()
        # (grid_bar_id) coordinates:
        # 0   1   2   3
        # 4   5   6   7
        # 8   9   10  11
        # 12  13  14  15
        self.__grid_bars_ids__ = [[0, 1, 4, 5],
                                  [2, 3, 6, 7],
                                  [8, 9, 12, 13],
                                  [10, 11, 14, 15]]
        self.__bars_to_display__ = []
        self.__render_options__ = self.__calculate_render_options__()

    def set_bars_to_display(self,
                            bars_to_display: List[Bar]) -> None:
        """
        Set bars of trial to display and repaint page.

        :params bars_to_display: Bars ot display.
        """
        self.__bars_to_display__ = bars_to_display
        self.repaint()

    def resizeEvent(self,
                    e: QResizeEvent) -> None:
        """
        Recalculate '__render_options__' on resizeEvent.

        :param e: QResizeEvent.
        """
        self.__render_options__ = self.__calculate_render_options__()

    def paintEvent(self,
                   e: QPaintEvent) -> None:
        """
        Render all '__bars_to_display__' at paintEvent.

        :param e: QPaintEvent.
        """
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

    def __calculate_render_options__(self) -> RenderOptions:
        """
        Calculate render options based on page size.

        :return: Render options.
        """
        ww = self.size().width()
        wh = self.size().height()
        self.setGeometry(0, 0, ww, wh)
        ro = RenderOptions()
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
        return ro

    def __generate_bar_rect__(self,
                              bar: Bar) -> Tuple[int, int, int, int]:
        """
        Generate (x; y; width; height) render coordinates of bar to display.

        :param bar: Bar to display.

        :return: (x; y; width; height) render coordinates.
        """
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
