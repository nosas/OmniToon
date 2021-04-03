from __future__ import annotations

from abc import ABC, abstractmethod
from random import choice as rand_choice

from .Cog import Cog
from .Exceptions import Error
from .Toon import Toon


class BattleContext:

    def __init__(self, state: BattleState, cogs: list[Cog], toons: list[Toon],
                 rewards: dict[Toon:int]) -> None:
        # ! Battle should always begin at ToonAttackState
        print("[^] Initializing BattleContext...")
        self.cogs = cogs
        self.toons = toons
        self.rewards = rewards

        self._completed_states = []

        self.state = state
        self.state.context = self

    @property
    def state(self) -> BattleState:
        return self._state

    @state.setter
    def state(self, new_state: BattleState) -> None:
        # print(f"        [>] Setting new state: {new_state}")
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
        self._completed_states.append(self.state)
        self.state = new_state
        print(f"        [-] `transition_to` completed states : {[str(state) for state in self._completed_states]}")  # noqa
        self.state.context = self

    def update(self):
        print(f"[+] BattleContext `update` pre-update state : {self.state}")
        if issubclass(self.state.__class__, AttackState):
            self.state.handle_attacks()
        elif issubclass(self.state.__class__, WinLoseState):
            self.state.handle_win_lose()
        elif type(self.state) == EndState:
            pass
        else:
            raise TypeError(self.state)
        print(f"    [-] BattleContext `update` post-update state : {self.state}")


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
        raise NotImplementedError

    def __init__(self):
        raise Exception("[!] ERROR: Entering state: AttackState")


class WinLoseState(BattleState):

    @abstractmethod
    def handle_win_lose():
        raise NotImplementedError

    def __init__(self):
        raise Exception("[!] ERROR: Entering state: WinLoseState")

    # TODO : Implement methods to calculate rewards, add rewards, level up Toon


# Do we need a ToonChooseAttack state and ToonDoAttack state? Likely yes, will
# be easier to debug and tweak decision-making of the AI.
# Will also make it easier to implement Strategy design pattern
class ToonAttackState(AttackState):

    def __init__(self):
        self.attacks = {}
        self.rewards = {}
        # ! ToonAtkState : If all Cogs defeated -> WinState else CogAtkState

    def handle_attacks(self):
        # TODO #44, Group and order attacks by Gag.track rather than sequntial
        for toon in self.context.toons:
            target_cog = rand_choice(self.context.cogs)
            print(f"    [+] ToonAttackState 'handle_attacks' : Toon {toon} is "
                  f"attacking Cog {target_cog}")

            gag_atk = toon.choose_attack(target=target_cog)
            atk_hit = toon.do_attack(target=target_cog, gag_atk=gag_atk)
            # Attack doesn't miss and Gag is eligible for reward
            if atk_hit and gag_atk.level < target_cog.level:
                self.attacks[toon] = gag_atk
                self.rewards[toon] = gag_atk.level + 1

        if all([cog.is_defeated() for cog in self.context.cogs]):
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
        for cog in self.context.cogs:
            target_toon = rand_choice(self.context.toons)
            print(f"    [+] CogAttackState 'handle_attacks' : Cog {cog} is "
                  f"attacking Toon {target_toon}")
            cog_atk = cog.choose_attack()
            atk_hit = cog.do_attack(target=target_toon, amount=cog_atk)

        # ! CogAtkState : If all Toons defeated -> LoseState else ToonAtkState
        if all([toon.is_defeated() for toon in self.context.toons]):
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

        # self.reward = self.calculate_rewards()
        # total_reward = sum(state.reward for state in self.reward)
        # print(f"[$] Total Reward = {total_reward}")

        if all([cog.is_defeated() for cog in self.context.cogs]):
            transition_state = EndState
        else:
            raise Error("We should be in EndState")
        self.context.transition_to(new_state=transition_state())


class LoseState(WinLoseState):
    # TODO : Implement methods to calculate rewards, remove all of Toon's Gags
    # TODO #9, implement functionality & create tests for Toon losing to Cog

    # Need an __init__ function, otherwise it'll initialize as an WinLoseState
    def __init__(self):
        super()

    def handle_win_lose(self):
        # TODO #11, replace this double for-loop with Gag objects
        # TODO Alternatively, make Toon.is_defeated() a property, strip all the
        # Gags in the setter method if Toon.is_defeated is True
        defeated_toons = [
            toon for toon in self.context._toons if toon.is_defeated()]

        for toon in defeated_toons:
            for track_idx, gag_track in enumerate(toon.gags):
                for gag_idx, gag in enumerate(toon.gags[track_idx]):
                    # Set the Gag count to 0 if the Gag is unlocked, or leave
                    # the Gag locked
                    toon.gags[track_idx][gag_idx] = 0 if gag != -1 else -1

        self.context.reward = [0]*7
        self.context.transition_to(new_state=EndState())


class EndState(BattleState):
    pass
