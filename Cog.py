from Entity import Entity


class Cog(Entity):
    def __init__(self, name, hp, level):
        super().__init__(name=name, hp=hp)
        self.name = name
        self.level = level
        self.hp = hp
