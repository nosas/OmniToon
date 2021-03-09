class Entity:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def _get_attacked(self, amount: int):
        self.hp -= amount

    # ? Why can't methods reference their own Class Types when type-hinting?
    # def do_attack(self, target: Entity, amount: int):
    def do_attack(self, target, amount: int):
        # TODO : Add chance_to_hit argument?
        target._get_attacked(amount=amount)
        return 1

    def get_name(self):
        return self.name

    def is_defeated(self):
        return self.hp <= 0
