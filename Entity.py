class Entity:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def do_attack(self, target: Entity, amount: int):
        target.get_attacked(amount=amount)

    def get_attacked(self, amount: int):
        self.hp -= amount

    def get_name(self):
        return self.name

    def is_dead(self):
        return self.hp > 0
