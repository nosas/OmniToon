from .Toon import Toon
from .Cog import Cog
from .BattleState import (
    BattleContext, BattleState, AttackState, WinLoseState,
    ToonAttackState, CogAttackState, WinState, LoseState
)


# TODO Create BattleCogBuilding w/ constructor accepting multi-toon&cogs
# TODO Look into Strategy design patterns for Toon decision making
# TODO Different strategies: max_reward, asap_win_ignore_reward, survive, etc.
# Pass: Clicking on PASS lets you skip your turn. Since Cogs will attack the
# Toon who has done him the most damage, you are less likely to be attacked
# if you choose Pass. This is a good strategy in a group battle if your Laff
# points are dangerously low.

# ! TODO Implement State design pattern, create BattleStates:
# ! e.g. ToonAttackState, CogAttackState, BattleWinState, BattleLoseState
class Battle:

    # Countdown timer for the Toon[s] to select a Gag and Target, or escape
    # Cog[s] will attack if no Gag and Target is provided by the Toon[s]
    countdown_timer = 99

    def __init__(self, first_cog: Cog, first_toon: Toon):
        self._states = []
        self._reward = 0
        self._context = BattleContext(state=ToonAttackState(),
                                      cogs=[first_cog],
                                      toons=[first_toon],
                                      reward=self._reward)

    @property
    def cogs(self):
        return self._context.cogs

    @property
    def toons(self):
        return self._context.toons

    def add_cog(self, new_cog: Cog):
        self.context.add_cog(new_cog)
        # self._cogs.append(new_cog)

    def add_toon(self, new_toon: Toon):
        self.context.add_toon(new_toon)
        # self._toons.append(new_toon)

    def calculate_rewards(self):
        if self.state == LoseState:
            self._reward = 0
        else:
            reward_states = [state for state in self._states if
                             type(state) == ToonAttackState]
            self._reward = sum(state.reward for state in reward_states)
        return self._reward

    def update(self):
        self._context.update()
