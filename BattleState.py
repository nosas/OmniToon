from __future__ import annotations

from abc import ABC, abstractmethod
from random import choice as rand_choice

from .Cog import Cog
from .Exceptions import Error, TooManyCogsError, TooManyToonsError
from .GagGlobals import LURE_TRACK, get_gag_track_name
from .Toon import Toon


class BattleContext:

    def __init__(self, state: BattleState, cogs: list[Cog], toons: list[Toon],
                 rewards: dict[Toon:dict[int:int]]) -> None:
        # ! Battle should always begin at ToonAttackState
        print("\n[^] Initializing BattleContext...")
        self.cogs = cogs
        self.toons = toons
        self.rewards = rewards

        self._completed_states = []

        self.state = state
        self.state.context = self

    def __str__(self) -> str:
        return self.__class__.__name__

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
        if len(cogs) > 4:
            raise TooManyCogsError
        assert all([type(x) == Cog for x in cogs])
        self._cogs = cogs

    @property
    def toons(self) -> list:
        return self._toons

    @toons.setter
    def toons(self, toons: list[Toon]) -> list:
        if len(toons) > 4:
            raise TooManyToonsError
        assert all([type(x) == Toon for x in toons])
        self._toons = toons

    def add_cog(self, new_cog: Cog) -> None:
        assert type(new_cog) == Cog
        if len(self._cogs) == 4:
            raise TooManyCogsError(new_cog)
        self._cogs.append(new_cog)

    def add_toon(self, new_toon: Toon) -> None:
        assert type(new_toon) == Toon
        if len(self._toons) == 4:
            raise TooManyToonsError(new_toon)
        self._toons.append(new_toon)

    def remove_cog(self, defeated_cog: Cog) -> None:
        assert type(defeated_cog) == Cog
        print(f"            [-] Cog {defeated_cog} is defeated")
        self.cogs.remove(defeated_cog)

    def transition_to(self, new_state: BattleState):
        print(f"    [+] `transition_to()` transition : {self.state} -> {new_state}")  # noqa
        self._completed_states.append(self.state)
        self.state = new_state
        print(f"        [-] `transition_to()` completed states : {[str(state) for state in self._completed_states]}")  # noqa
        self.state.context = self

    def update(self):
        print(f"[+] {self} `update()` pre-update state : {self.state}")

        if issubclass(self.state.__class__, AttackState):
            print(f"    [+] `handle_attacks()` {self.state} ")
            self.state.handle_attacks()
        elif issubclass(self.state.__class__, WinLoseState):
            print(f"    [+] `handle_win_lose()` {self.state} ")
            self.state.handle_win_lose()
        elif type(self.state) == EndState:
            print(f"    [$] Do we want to do anything in {self.state}?")
            pass  # ? Do we want to do anything in EndState?
        else:
            raise TypeError(self.state)

        print(f"    [-] {self} `update()` post-update state : {self.state}")  # noqa


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

    # TODO #37, #45: Implement methods to add rewards, level up Toon


# Do we need a ToonChooseAttack state and ToonDoAttack state? Likely yes, will
# be easier to debug and tweak decision-making of the AI.
# Will also make it easier to implement Strategy design pattern
class ToonAttackState(AttackState):

    def __init__(self):
        self.attacks = []  # [(Toon, Cog, Gag, atk_hit_or_miss: int [0|1])]
        # ! ToonAtkState : If all Cogs defeated -> WinState else CogAtkState
        # TODO #51, Add bonus EXP multipliers as a ToonAttackState property

    def handle_attacks(self):
        potential_attacks = {}

        # TODO #44, Group and order attacks by Gag.track rather than sequential
        # Select Targets
        for toon in self.context.toons:
            target_cog = rand_choice(self.context.cogs)
            print(f"        [+] Toon {toon} targets Cog {target_cog}")

            gag_atk = toon.choose_attack(target=target_cog)
            # TODO #44, Group and order attacks by Gag.track
            if gag_atk.track not in potential_attacks:
                potential_attacks[gag_atk.track] = []
            potential_attacks[gag_atk.track].append((toon, gag_atk))

        # Do attack in order, sorted from lowest GagTrack index to highest
        for gag_track in sorted(potential_attacks):
            # TODO #20, Calculate bonus damage
            highest_accuracy = max(gag.accuracy for _, gag in potential_attacks[gag_track])
            total_damage = sum(gag.damage for _, gag in potential_attacks[gag_track])

            print(f"        [>] Gag Track : {get_gag_track_name(gag_track)}")
            for toon, gag_atk in potential_attacks[gag_track]:
                # TODO #10, Add chance_to_hit
                atk_hit = toon.do_attack(target=target_cog, gag_atk=gag_atk,
                                         overdefeat=True)
                self.attacks.append((toon, target_cog, gag_atk, atk_hit))
                # Attack doesn't miss and Gag is eligible for reward
                if atk_hit:
                    # Execute the Trap gag if the Toon lures a trapped Cog
                    if gag_atk.track == LURE_TRACK and target_cog.is_trapped:
                        trap_toon, trap_gag = target_cog.trap
                        # TODO #10, Add chance to hit == 100
                        trap_toon.do_attack(target=target_cog, gag_atk=trap_gag)  # noqa
                        self.attacks.append((trap_toon, target_cog, gag_atk, atk_hit))  # noqa

            if target_cog.is_defeated:
                self.context.remove_cog(defeated_cog=target_cog)
                break

        if all([cog.is_defeated for cog in self.context.cogs]):
            # ! First need to check if all cogs defeated, then battle is Won
            transition_state = WinState
        else:
            transition_state = CogAttackState
        self.context.transition_to(new_state=transition_state())


class CogAttackState(AttackState):

    def __init__(self):
        self.attacks = {}  # {Cog: (Toon, Damage)}

    def handle_attacks(self):
        for cog in self.context.cogs:
            viable_toons = [
                toon for toon in self.context.toons if not toon.is_defeated]
            target_toon = rand_choice(viable_toons)
            print(f"        [+] {self} Cog {cog} targets Toon {target_toon}")
            cog_atk = cog.choose_attack()
            atk_hit = cog.do_attack(target=target_toon, amount=cog_atk['hp'])
            self.attacks[cog] = (target_toon, cog_atk, atk_hit)

            if target_toon.is_defeated:
                print(f"            [-] Toon {target_toon} is defeated")
                # ! If all Toons defeated -> LoseState else ToonAtkState
                if all([toon.is_defeated for toon in self.context.toons]):
                    transition_state = LoseState
                    break
            else:
                transition_state = ToonAttackState

        self.context.transition_to(new_state=transition_state())


class WinState(WinLoseState):

    # Need an __init__ function, otherwise it'll initialize as an WinLoseState
    def __init__(self):
        super()

    def handle_win_lose(self):
        """ # TODO #9, #37, #46
        * 1. If attack hits and all Cogs are defeated, calculate EXP and add to
        *    gag track EXP (AI reward)

        * 2. Add EXP multiplier (cog building, invasions)
        """
        print("        [-] TODO #9, #37, #46")
        # self.reward = self.calculate_rewards()
        # total_reward = sum(state.reward for state in self.reward)
        # print(f"[$] Total Reward = {total_reward}")

        if all([cog.is_defeated for cog in self.context.cogs]):
            transition_state = EndState
        else:
            raise Error("We should be in EndState")
        self.context.transition_to(new_state=transition_state())


class LoseState(WinLoseState):
    # TODO #37, #45: Implement methods to calculate rewards, remove Toon's Gags
    # TODO #9, implement functionality & create tests for Toon losing to Cog

    # Need an __init__ function, otherwise it'll initialize as an WinLoseState
    def __init__(self):
        super()

    def handle_win_lose(self):
        # TODO #11, replace this double for-loop with Gag objects
        # TODO Alternatively, make Toon.is_defeated a property, strip all the
        # Gags in the setter method if Toon.is_defeated is True
        defeated_toons = [
            toon for toon in self.context._toons if toon.is_defeated]

        for toon in defeated_toons:
            print(f"        [-] Removing all Gags from Toon {toon}")
            for track_idx, gag_track in enumerate(toon.gags):
                for gag_idx, gag in enumerate(toon.gags[track_idx]):
                    # Set the Gag count to 0 if the Gag is unlocked, or leave
                    # the Gag locked
                    toon.gags[track_idx][gag_idx] = 0 if gag != -1 else -1

        self.context.reward = [0]*7
        self.context.transition_to(new_state=EndState())


class EndState(BattleState):
    pass
