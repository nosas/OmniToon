from .BattleState import BattleContext, EndState, ToonAttackState
from .Cog import Cog
from .Toon import Toon

# TODO Create BattleCogBuilding w/ constructor accepting multi-toon&cogs
# TODO Look into Strategy design patterns for Toon decision making
# TODO #38 Different strategies: max_reward, fast_win_ignore_reward, survive..
# Pass: Clicking on PASS lets you skip your turn. Since Cogs will attack the
# Toon who has done him the most damage, you are less likely to be attacked
# if you choose Pass. This is a good strategy in a group battle if your Laff
# points are dangerously low.


class Battle:

    # Countdown timer for the Toon[s] to select a Gag and Target, or escape
    # Cog[s] will attack if no Gag and Target is provided by the Toon[s]
    countdown_timer = 99

    def __init__(self, first_cog: Cog, first_toon: Toon):
        # self._reward = [0]*7
        self._rewards = {first_toon: [0]*7}
        self._states = []
        self._context = BattleContext(state=ToonAttackState(),
                                      cogs=[first_cog],
                                      toons=[first_toon],
                                      rewards=self._rewards)
        self.is_battling = True

    @property
    def context(self):
        return self._context

    @property
    def cogs(self):
        return self._context.cogs

    @property
    def toons(self):
        return self._context.toons

    def add_cog(self, new_cog: Cog):
        self.context.add_cog(new_cog)

    def add_toon(self, new_toon: Toon):
        self.context.add_toon(new_toon)
        self._rewards[new_toon] = [0]*7

    def calculate_rewards(self) -> list:
        import pprint  # To make rewards output readable
        pp = pprint.PrettyPrinter(indent=1)

        toon_attack_states = [
            state for state in self.context._completed_states if
            type(state) == ToonAttackState
        ]

        # Sum rewards for all Toons
        for toon in self.toons:
            # If Toon is defeat, no rewards are given
            if toon.is_defeated():
                self._rewards[toon] = [0]*7
                continue

            print(f"    [+] `calculate_rewards` for Toon {toon}")
            for attack_state in toon_attack_states:
                if toon in attack_state.attacks:
                    gag = attack_state.attacks[toon]
                    reward = attack_state.rewards[toon]
                    self._rewards[toon][gag.track] += reward
                    print(f"        [>] +{reward} {gag.track_name} exp ({gag})")  # noqa
            print(f"        [-] Total rewards for Toon {toon} : "
                  f"{self._rewards[toon]}")

        print(f"[$] `calculate_rewards` total rewards all Toons : "
              f"{self._rewards}")
        pp.pprint(self._rewards)

        return self._rewards

    def update(self):
        self.context.update()
        if type(self.context.state) == EndState:
            print(f"[+] Battle `update` : Calculating rewards")
            self.is_battling = False
