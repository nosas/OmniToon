from Entity import Entity
from Cog import Cog
from Gag import Gag



class Toon(Entity):
    def __init__(self, name, health):
        """
        Initialize Toon with a name (str), health (int), gags (dict)

        """
        self.name = name
        self.health = health
        # self.gags = get_available_gags(self.name)
        # Possible States: Dead (0), Battle (1), Heal (2)
        self.state = None

    def do_attack(self, target: Cog, gag: Gag) -> None:
        # TODO : Return 1 if hit, 0 if miss?
        super().do_attack(target=target, amount=gag.damage)
