from .BattleState import BattleContext, ToonAttackState, WinState
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
        self._reward = [0]*7
        self._states = []
        self._context = BattleContext(state=ToonAttackState(),
                                      cogs=[first_cog],
                                      toons=[first_toon],
                                      reward=self._reward)

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

    def calculate_rewards(self) -> list:
        if type(self.context.state) == WinState:
            reward_states = [
                (state.gag_atk, state.reward) for state in
                self.context._completed_states if
                type(state) == ToonAttackState
            ]

            for gag, reward in reward_states:
                self._reward[gag.track] += reward

            import pprint
            pp = pprint.PrettyPrinter(indent=1)
            print(f"[$] `calculate_rewards` attack states : ")
            pp.pprint(reward_states)

        print(f"[$] `calculate_rewards` total rewards : {self._reward}")
        return self._reward

    def update(self):
        self.context.update()
