from __future__ import annotations
from abc import ABC, abstractmethod
from .Cog import Cog
from .GagGlobals import THROW_TRACK
from .Toon import Toon


class BattleContext:

    _state = None

    def __init__(self, state: BattleState, cogs: list[Cog], toons: list[Toon],
                 reward: int) -> None:
        # ! Battle should always begin at ToonAttackState
        self._cogs = cogs
        self._toons = toons
        self.reward = reward
        self.transition_to(state)

    @property
    def cogs(self) -> list:
        return self._cogs

    @cogs.setter
    def cogs(self, cogs: list[Cog]) -> None:
        assert all([type(x) == Cog for x in cogs])
        self._cogs = cogs

    @property
    def toons(self) -> list:
        return self._toons

    @toons.setter
    def toons(self, toons: list[Toon]) -> list:
        assert all([type(x) == Toon for x in toons])
        self._toons = toons

    def add_cog(self, new_cog: Cog) -> None:
        assert type(new_cog) == Cog
        self._cogs.append(new_cog)

    def add_toon(self, new_toon: Toon) -> None:
        assert type(new_toon) == Toon
        self._toons.append(new_toon)

    def transition_to(self, state: BattleState):
        self._state = state
        self._state.context = self

    def update(self):
        state_type = type(self._state)

        if state_type in [ToonAttackState, CogAttackState]:
            self._state.handle_attacks()
        elif state_type in [WinState, LoseState]:
            self._state.handle_win_lose()
        else:
            raise TypeError(state_type)


class BattleState(ABC):

    @property
    def context(self) -> BattleContext:
        return self._context

    @context.setter
    def context(self, context: BattleContext) -> None:
        self._context = context


class AttackState(BattleState):

    @abstractmethod
    def handle_attacks(self):
        pass

    def __init__(self):
        print("[!] ERROR: Entering state: BattleState")


class WinLoseState(BattleState):

    @abstractmethod
    def handle_win_lose(self):
        pass

    def __init__(self):
        print("[!] ERROR: Entering state: WinLoseState")


# Do we need a ToonChooseAttack state and ToonDoAttack state? Likely yes, will
# be easier to debug and tweak decision-making of the AI.
# Will also make it easier to implement Strategy design pattern
class ToonAttackState(AttackState):

    def __init__(self):
        print("[!] Entering state: ToonAttackState")
        # ! ToonAtkState : If all Cogs defeated -> WinState else CogAtkState

    def handle_attacks(self):
        print("[!] AttackState 'handle_attacks' is attacking the 1st Cog")
        my_toon = self.context.toons[0]
        target_cog = self.context.cogs[0]
        # target_cog.hp = 100
        # TODO Create function/overload to randomly choose attack
        my_toon.do_attack(target=target_cog,
                          gag_track=THROW_TRACK,
                          gag_level=1)

        if target_cog.is_defeated():
            # ! First need to check if all cogs defeated, then battle is Won
            transition_state = WinState
        else:
            transition_state = CogAttackState
        self.context.transition_to(state=transition_state())


class CogAttackState(AttackState):

    def __init__(self):
        # ! CogAtkState : If all Toons defeated -> LoseState else ToonAtkState
        # ! These print statements aren't going to cut it, time to start logs!
        # Will likely need an Observer class, which might be needed anyways
        print("[!] Entering state: CogAttackState")

    def handle_attacks(self):
        pass


class WinState(WinLoseState):

    def __init__(self):
        print("[!] Entering state: WinState")
        """ # TODO
        * 1. If attack hits and all Cogs are defeated, calculate EXP and add to
        *    gag track EXP (AI reward)

        * 2. Add EXP multiplier (cog building, invasions)
        """

    def handle_win_lose(self):
        return super().handle_win_lose()


class LoseState(WinLoseState):

    def __init__(self):
        print("[!] Entering state: LoseState")

    def handle_win_lose(self):
        return super().handle_win_lose()


class EndState(BattleState):
    pass
