from enum import Enum


class ExtraSmallSize:
    WIDTH=3
    HEIGHT=2


class SmallSize:
    WIDTH=4
    HEIGHT=3


class MediumSize:
    WIDTH=6
    HEIGHT=4


class LargeSize:
    WIDTH=9
    HEIGHT=6


class ExtraLargeSize:
    WIDTH=12
    HEIGHT=8
    

class SizeType(Enum):
    EXTRA_SMALL=ExtraSmallSize()
    SMALL=SmallSize()
    MEDIUM=MediumSize()
    LARGE=LargeSize()
    EXTRA_LARGE=ExtraLargeSize()