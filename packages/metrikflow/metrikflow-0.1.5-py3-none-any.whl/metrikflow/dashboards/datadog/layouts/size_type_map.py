from typing import Dict, Union, Literal
from .size_type import (
    SizeType,
    ExtraSmallSize,
    SmallSize,
    MediumSize,
    LargeSize,
    ExtraLargeSize
)


class SizeTypeMap:

    def __init__(self) -> None:
        self._types: Dict[
            str, 
            Union[
                ExtraSmallSize,
                SmallSize,
                MediumSize,
                LargeSize,
                ExtraLargeSize
            ]
        ] = {
            'extra_small': SizeType.EXTRA_SMALL.value,
            'small': SizeType.SMALL.value,
            'medium': SizeType.MEDIUM.value,
            'large': SizeType.LARGE.value,
            'extra_large': SizeType.EXTRA_LARGE.value
        }

        self._width_map: Dict[
            int, 
            Union[
                ExtraSmallSize,
                SmallSize,
                MediumSize,
                LargeSize,
                ExtraLargeSize
            ]
        ] = {
            3: SizeType.EXTRA_SMALL.value,
            4: SizeType.SMALL.value,
            6: SizeType.MEDIUM.value,
            9: SizeType.LARGE.value,
            12: SizeType.EXTRA_LARGE.value
        }

    def __getitem__(
        self, 
        size_type: Union[
            Literal['extra_small'],
            Literal['small'],
            Literal['medium'],
            Literal['large'],
            Literal['extra_large']
        ]
    ):
        return self._types.get(
            size_type,
            SizeType.MEDIUM.value
        )
    
    def get(
        self, 
        size_type: Union[
            Literal['extra_small'],
            Literal['small'],
            Literal['medium'],
            Literal['large'],
            Literal['extra_large']
        ]
    ):
        return self._types.get(size_type)
    
    def get_by_width(
        self, 
        width: Union[
            Literal[3],
            Literal[4],
            Literal[6],
            Literal[9],
            Literal[12]
        ]
    ):
        return self._width_map.get(width)
    

    