from enum import Enum


# ATK_TGT_UNKNOWN, ATK_TGT_SINGLE, ATK_TGT_MULTI = (0, 1, 2)  # previously 1,2,3
class GROUP(Enum):
    UNKNOWN = 0
    SINGLE = 1
    MULTI = 2


# IntEnums do not support float
class MULTIPLIER:

    FLOOR1 = 1.0
    FLOOR2 = 1.5
    FLOOR3 = 2.0
    FLOOR4 = 2.5
    FLOOR5 = 3.0
    NO_INVASION = 1.0
    INVASION = 2.0

    @staticmethod
    def get_building_multiplier_from_floor(floor: int) -> float:
        # return [MULTIPLIER.FLOOR1, MULTIPLIER.FLOOR2, MULTIPLIER.FLOOR3,
        #         MULTIPLIER.FLOOR4, MULTIPLIER.FLOOR5][floor - 1]
        return ((0.5 * floor) + 0.5)


MULTIPLIER_DEFAULT = int(MULTIPLIER.FLOOR1 * MULTIPLIER.NO_INVASION)
