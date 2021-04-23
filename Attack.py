
ATK_TGT_UNKNOWN, ATK_TGT_SINGLE, ATK_TGT_MULTI = (0, 1, 2)  # previously 1,2,3


class Attack():
    def __init__(self, name: str, damage: int, accuracy: int,
                 target: int = ATK_TGT_UNKNOWN):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy
        self.target = target
