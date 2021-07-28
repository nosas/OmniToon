from enum import Enum


# ATK_TGT_UNKNOWN, ATK_TGT_SINGLE, ATK_TGT_MULTI = (0, 1, 2)  # previously 1,2,3
class GROUP(Enum):
    UNKNOWN = 0
    SINGLE = 1
    MULTI = 2


class MULTIPLIER(Enum):
    FLOOR1 = 1
    FLOOR2 = 2
    FLOOR3 = 3
    FLOOR4 = 4
    FLOOR5 = 5
    INVASION = 2
