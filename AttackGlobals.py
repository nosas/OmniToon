from enum import Enum


# ATK_TGT_UNKNOWN, ATK_TGT_SINGLE, ATK_TGT_MULTI = (0, 1, 2)  # previously 1,2,3
class GROUP(Enum):
    UNKNOWN = 0
    SINGLE = 1
    MULTI = 2
