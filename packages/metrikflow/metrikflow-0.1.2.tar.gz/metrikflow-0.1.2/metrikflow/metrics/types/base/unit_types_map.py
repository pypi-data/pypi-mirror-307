from typing import Literal, Dict
from .unit_type import UnitType


class UnitTypesMap:

    def __init__(self) -> None:
        self._types: Dict[
            Literal[
                'nanoseconds',
                'microseconds',
                'milliseconds',
                'seconds',
                'minutes',
                'hours',
                'days',
                'weeks'
            ],
            UnitType
        ] = {
            'nanoseconds': UnitType.NANOSECONDS,
            'microseconds': UnitType.MICROSECONDS,
            'milliseconds': UnitType.MILLISECONDS,
            'seconds': UnitType.SECONDS,
            'minutes': UnitType.MINUTES,
            'hours': UnitType.HOURS,
            'days': UnitType.DAYS,
            'weeks': UnitType.WEEKS
        }

    def __getitem__(
        self,
        unit_type: Literal[
            'nanoseconds',
            'microseconds',
            'milliseconds',
            'seconds',
            'minutes',
            'hours',
            'days',
            'weeks'
        ]
    ):
        return self._types.get(unit_type)

    def get(
        self,
        unit_type: Literal[
            'nanoseconds',
            'microseconds',
            'milliseconds',
            'seconds',
            'minutes',
            'hours',
            'days',
            'weeks'
        ] 
    ):
        return self._types.get(unit_type)