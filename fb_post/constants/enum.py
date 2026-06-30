from enum import Enum

from ib_common.constants import BaseEnumClass


class ReactionTypeEnum(BaseEnumClass, Enum):
    WOW = "WOW"
    LIT = "LIT"
    LOVE = "LOVE"
    HAHA = "HAHA"
    THUMBS_UP = "THUMBS-UP"
    THUMBS_DOWN = "THUMBS-DOWN"
    ANGRY = "ANGRY"
    SAD = "SAD"