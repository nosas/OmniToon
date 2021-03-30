from __future__ import annotations

from abc import ABC, abstractmethod

from .Cog import Cog
from .Toon import Toon


class BattleContext:

    _state = None
    _completed_states = []

    def __init__(self, state: BattleState, cogs: list[Cog], toons: list[Toon],
                 reward: int) -> None:
        # ! Battle should always begin at ToonAttackState
        print("[^] Initializing BattleContext...")
        self._cogs = cogs
        self._toons = toons
        self.reward = reward
        self.transition_to(state)

    @property
    def state(self) -> BattleState:
        return self._state

    @state.setter
    def state(self, new_state: BattleState) -> None:
        print(f"        [>] Setting new state: {new_state}")
        if self.state:  # Don't append initial None value
            self._completed_states.append(self.state)
        self._state = new_state

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

    def transition_to(self, new_state: BattleState):
        print(f"    [+] `transition_to` transition : {self.state} -> {new_state}")  # noqa
        self.state = new_state
        print(f"        [-] `transition_to` states : {[str(state) for state in self._completed_states]}")  # noqa
        self.state.context = self

    def update(self):
        print(f"[+] `update` pre-update state : {self.state}")
        if issubclass(self.state.__class__, AttackState):
            self.state.handle_attacks()
        elif issubclass(self.state.__class__, WinLoseState):
            self.state.handle_win_lose()
        else:
            raise TypeError(self.state)
        print(f"    [-] `update` post-update state : {self.state}")


class BattleState(ABC):

    @property
    def context(self) -> BattleContext:
        return self._context

    @context.setter
    def context(self, context: BattleContext) -> None:
        self._context = context

    def __str__(self) -> str:
        return self.__class__.__name__


class AttackState(BattleState):

    @abstractmethod
    def handle_attacks():
        pass

    def __init__(self):
        raise Exception("[!] ERROR: Entering state: AttackState")


class WinLoseState(BattleState):

    @abstractmethod
    def handle_win_lose():
        pass

    def __init__(self):
        raise Exception("[!] ERROR: Entering state: WinLoseState")


# Do we need a ToonChooseAttack state and ToonDoAttack state? Likely yes, will
# be easier to debug and tweak decision-making of the AI.
# Will also make it easier to implement Strategy design pattern
class ToonAttackState(AttackState):

    def __init__(self):
        self.gag_atk = None
        self.reward = 0
        # ! ToonAtkState : If all Cogs defeated -> WinState else CogAtkState

    def handle_attacks(self):
        my_toon = self.context.toons[0]
        target_cog = self.context.cogs[0]
        print(f"    [+] ToonAttackState 'handle_attacks' : Toon {my_toon} is "
              f"attacking Cog {target_cog}")

        self.gag_atk = my_toon.choose_attack(target=target_cog)
        atk_hit = my_toon.do_attack(target=target_cog, gag_atk=self.gag_atk)
        # Attack doesn't miss and Gag is eligible for reward
        if atk_hit and self.gag_atk.level < target_cog.level:
            self.reward = self.gag_atk.level + 1

        if target_cog.is_defeated():
            # ! First need to check if all cogs defeated, then battle is Won
            transition_state = WinState
        else:
            transition_state = CogAttackState
        self.context.transition_to(new_state=transition_state())


class CogAttackState(AttackState):

    # Need an __init__ function, otherwise it'll initialize as an AttackState
    def __init__(self):
        super()

    def handle_attacks(self):
        my_toon = self.context.toons[0]
        target_cog = self.context.cogs[0]
        print(f"    [+] CogAttackState 'handle_attacks' : Cog {target_cog} is "
              f"attacking Toon {my_toon}")

        cog_atk = target_cog.choose_attack()
        atk_hit = target_cog.do_attack(target=my_toon, amount=cog_atk)

        # ! CogAtkState : If all Toons defeated -> LoseState else ToonAtkState
        if my_toon.is_defeated():
            transition_state = LoseState
        else:
            transition_state = ToonAttackState
        self.context.transition_to(new_state=transition_state())


class WinState(WinLoseState):

    # Need an __init__ function, otherwise it'll initialize as an WinLoseState
    def __init__(self):
        super()

    def handle_win_lose(self):
        """ # TODO #9, #37
        * 1. If attack hits and all Cogs are defeated, calculate EXP and add to
        *    gag track EXP (AI reward)

        * 2. Add EXP multiplier (cog building, invasions)
        """
        reward_states = [state for state in self.context._completed_states
                         if type(state) == ToonAttackState]
        reward = sum(state.reward for state in reward_states)
        print(f"[$] Reward = {reward}")
        return reward
        # return super().handle_win_lose()


class LoseState(WinLoseState):
    # TODO #9, implement functionality & create tests for Toon losing to Cog

    # Need an __init__ function, otherwise it'll initialize as an WinLoseState
    def __init__(self):
        super()

    def handle_win_lose():
        return super().handle_win_lose()


class EndState(BattleState):
    pass
