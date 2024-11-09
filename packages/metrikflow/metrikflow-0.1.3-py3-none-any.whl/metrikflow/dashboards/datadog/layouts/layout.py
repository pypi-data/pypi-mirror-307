from datadog_api_client.v1.model.widget_layout import WidgetLayout
from typing import List, Union, Literal, Dict
from .size_type import (
    ExtraLargeSize,
    SmallSize,
    MediumSize,
    LargeSize,
    ExtraLargeSize
)
from .size_type_map import (
    SizeTypeMap,
    ExtraSmallSize,
    SmallSize,
    MediumSize,
    LargeSize,
    ExtraLargeSize
)


class Layout:

    def __init__(self) -> None:
        self.MAX_ROW_WIDTH=12
        self._current_row_width = 0
        self._layout_matrix: List[List[WidgetLayout]] = []
        self._widgets: Dict[str, WidgetLayout] = {}
        self._current_row: List[WidgetLayout] = []
        self._current_row_height = 0

    @property
    def widget_layout(self):
        return self._layout_matrix
    
    def __getitem__(self, widget_name: str):
        return self._widgets.get(widget_name)

    def add_widget(
        self, 
        widget_title: str,
        widget_size: Union[
            ExtraLargeSize,
            SmallSize,
            MediumSize,
            LargeSize,
            ExtraLargeSize
        ]
    ):
        requested_row_width = self._current_row_width + widget_size.WIDTH

        # If adding the widget would put us over the max width and we still haven't filled the row,
        # increase the size of the widgets in the row so that the row is filled.
        if requested_row_width > self.MAX_ROW_WIDTH and self._current_row_width < self.MAX_ROW_WIDTH:
            # Find the difference between the max row width and current row width
            # then distribute the difference among the existing widgets.
            difference = self.MAX_ROW_WIDTH - self._current_row_width

            row_items_count = len(self._current_row)
            last_item_width_buff = difference%row_items_count

            width_buffs = [
                int(difference/row_items_count) for _ in range(row_items_count)
            ]

            width_buffs[-1] += last_item_width_buff

            for item, width_buff in zip(
                self._current_row, 
                width_buffs
            ):
                item.width += width_buff

            self._append_new_row(
                widget_title,
                widget_size
            )

        # If adding the widget would put us over the max width and all widgets
        # completely fill the row.
        elif requested_row_width > self.MAX_ROW_WIDTH:
            self._append_new_row(
                widget_title,
                widget_size
            )

        else:
            widget_layout = WidgetLayout(
                height=widget_size.HEIGHT,
                width=widget_size.WIDTH,
                x=self._current_row_width,
                y=self._current_row_height
            )

            self._current_row.append(widget_layout)
            self._widgets[widget_title] = widget_layout

            self._current_row_width += widget_size.WIDTH
            

    def _append_new_row(
        self,
        widget_title: str,
        widget_size: Union[
            ExtraSmallSize,
            SmallSize,
            MediumSize,
            LargeSize,
            ExtraLargeSize
        ]
    ):
        row_height = self._get_row_max_height()
        self._current_row_height += row_height

        # Set all widget heights to the max height for uniformity's
        # sake
        for item in self._current_row:
            item.height = row_height

        # Append all widgets in the the current row to the matrix
        self._layout_matrix.extend(self._current_row)

        # Get the max height of the current row as the starting
        # height for the next row and initialize a new row
        # with the new widget

        widget_layout = WidgetLayout(
            height=widget_size.HEIGHT,
            width=widget_size.WIDTH,
            x=0,
            y=self._current_row_height
        )

        self._current_row = [widget_layout]

        # Set the starting x position of the next widget as the
        # width of the current widget.
        self._current_row_width = widget_size.WIDTH

        self._widgets[widget_title] = widget_layout

    def _get_row_max_height(self):
        # Get the max height of the current row
        return max([
            item.height for item in self._current_row
        ])


        

                




        
        
