from collections import OrderedDict
from typing import List, Union

from tabulate import tabulate

from metrikflow.logging import MetrikflowLogger
from metrikflow.metrics.types import Event, Interval, Rate
from metrikflow.tools.formatting import seconds_to_human_string


class MetrikTable:

    def __init__(
        self,
        metrics: List[
            Union[
                Event, 
                Interval, 
                Rate
            ]
        ]
    ) -> None:
        
        self.table: Union[str, None] = None

        self.metrics = metrics
        self.table_rows: List[OrderedDict] = []

        self.logger = MetrikflowLogger()
        self.logger.initialize()

    def generate_table(self):

        for metric in self.metrics:
            table_row = OrderedDict()

            metric_data = metric.to_data_dict()

            for field_name in metric.to_column_names():
                header_name = field_name.replace('_', ' ')
                metric_value = metric_data[field_name]

                if field_name == 'value' and isinstance(metric, Interval):
                    metric_value = seconds_to_human_string(metric_value)

                table_row[header_name] = metric_value

            for tag_set in metric.tags:
                for tag_name, tag_value in tag_set.items():
                    table_row[tag_name] = tag_value

            self.table_rows.append(table_row)

        self.table = tabulate(
            self.table_rows,
            headers='keys',
            missingval='None',
            tablefmt="simple",
            floatfmt=".2f"
        )

        self.logger.console.sync.info('\nMetrics:\n')
        self.logger.console.sync.info(f'''{self.table}\n''')
