from metrik.metrics.types.base.unit_type import UnitType
from typing import Dict, Literal

class DatadogUnitMap:

    def __init__(self) -> None:
        self._unit_types: Dict[
            UnitType,
            Literal[
                'nanosecond',
                'microsecond',
                'millisecond',
                'second',
                'minute',
                'hour',
                'day',
                'week'
            ]
        ] = {
            UnitType.NANOSECONDS: 'nanosecond',
            UnitType.MICROSECONDS: 'microsecond',
            UnitType.MILLISECONDS: 'millisecond',
            UnitType.SECONDS: 'second',
            UnitType.MINUTES: 'minute',
            UnitType.HOURS: 'hour',
            UnitType.DAYS: 'day',
            UnitType.WEEKS: 'week'
        }

    def __getitem__(
        self,
        unit_type: UnitType
    ):
        return self._unit_types.get(
            unit_type,
            'second'
        )

    def get(
        self,
        unit_type: UnitType
    ):
        return self._unit_types.get(unit_type)