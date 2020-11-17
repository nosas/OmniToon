class Agent:
    def __init__(self, health, game):  # Takes game as input for taking actions
        self._health = health
        self._game = game
        self.available_attacks = []

    def is_battling(self):
        return self._game.get_battling()

    def get_health(self):
        return self._health()

    def attack(self, enemy):
        pass

    def heal(self, ally):
        pass
