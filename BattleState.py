from __future__ import annotations

from abc import ABC, abstractmethod
from random import choice as rand_choice

from .AttackGlobals import ATK_TGT_MULTI
from .Battle import BattleEntity
from .Exceptions import Error, TooManyCogsError, TooManyToonsError
from .Gag import get_gag_track_name


class BattleContext:

    def __init__(self, state: BattleState, cogs: list[BattleEntity], toons: list[BattleEntity],
                 rewards: dict[BattleEntity:dict[int:int]]) -> None:
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
    def cogs(self, cogs: list[BattleEntity]) -> None:
        if len(cogs) > 4:
            raise TooManyCogsError
        assert all([type(x) == BattleEntity for x in cogs])
        self._cogs = cogs

    @property
    def toons(self) -> list[BattleEntity]:
        return self._toons

    @toons.setter
    def toons(self, toons: list[BattleEntity]) -> list:
        if len(toons) > 4:
            raise TooManyToonsError
        assert all([type(x) == BattleEntity for x in toons])
        self._toons = toons

    def add_cog(self, new_cog: BattleEntity) -> None:
        assert type(new_cog) == BattleEntity
        if len(self._cogs) == 4:
            raise TooManyCogsError(new_cog)
        self._cogs.append(new_cog)

    def add_toon(self, new_toon: BattleEntity) -> None:
        assert type(new_toon) == BattleEntity
        if len(self._toons) == 4:
            raise TooManyToonsError(new_toon)
        self._toons.append(new_toon)

    def remove_cog(self, defeated_cog: BattleEntity) -> None:
        assert type(defeated_cog) == BattleEntity
        print(f"            [-] BattleEntity {defeated_cog} is defeated")
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

    # TODO #37, #45: Implement methods to add rewards, level up BattleEntity


# Do we need a ToonChooseAttack state and ToonDoAttack state? Likely yes, will
# be easier to debug and tweak decision-making of the AI.
# Will also make it easier to implement Strategy design pattern
class ToonAttackState(AttackState):

    # ! ToonAtkState : If all Cogs defeated -> WinState else CogAtkState
    def __init__(self):
        self.attacks = []  # [(BattleEntity, BattleEntity, Gag, atk_hit_or_miss: int [0|1])]
        # Keep track of which Cogs are being targeted and by how many Toons
        self.overdefeat_cogs = {}
        # TODO #51, Add bonus EXP multipliers as a ToonAttackState property

    def handle_attacks(self):
        potential_attacks = {}
        self.overdefeat_cogs = {cog: {} for cog in self.context.cogs}

        # #44, Group and order attacks by Gag.track rather than sequential
        # Select Targets and choose Gag Attacks
        for toon in self.context.toons:
            if toon.is_defeated:
                continue
            # TODO #40, choose_target
            """
            1. Get viable attacks against all Cogs
            2. Randomly pick one viable attack Gags list to use
                2a. Must have at least 1 viable Gag in the list
                2b. If no viable Gags available for any target, we pass/stall
            3. Randomly pick one attack from the viable Gags list
            """
            alive_cogs = [
                cog for cog in self.context.cogs if not cog.is_defeated]

            target_cogs, gag_atk = toon.choose_attack(targets=alive_cogs)
            print(f"            [-] BattleEntity {toon} targets BattleEntity {target_cogs}")
            # #44, Group attacks by Gag.track
            if gag_atk.track not in potential_attacks:
                potential_attacks[gag_atk.track] = []

            # Track which Cogs are being targeted and by how many Toons
            for target_cog in target_cogs:
                if gag_atk.track not in self.overdefeat_cogs[target_cog]:
                    self.overdefeat_cogs[target_cog][gag_atk.track] = 0
                self.overdefeat_cogs[target_cog][gag_atk.track] += 1

            potential_attack = (toon, target_cogs, gag_atk)
            potential_attacks[gag_atk.track].append(potential_attack)

        # #44, Do attacks in order, sorted ascending (low->high) GagTrack index
        for gag_track in sorted(potential_attacks):
            # TODO #20, Calculate bonus damage
            highest_accuracy = max(
                gag.accuracy for _, _, gag in potential_attacks[gag_track])
            total_damage = sum(
                gag.damage for _, _, gag in potential_attacks[gag_track])

            print(f"        [>] Gag Track : {get_gag_track_name(gag_track)}")
            for toon, target_cogs, gag_atk in potential_attacks[gag_track]:
                # If 2+ Toons are attacking the same BattleEntity with the same GagTrack
                #   Set overdefeat to True to override CogAlreadyDefeatedError
                for cog in target_cogs:
                    is_overdefeat = self.overdefeat_cogs[cog][gag_atk.track] > 1  # noqa
                    # Cache cog.trap.. if BattleEntity uses Lure and the Trap activates
                    cog_is_trapped = cog.is_trapped
                    if cog_is_trapped:
                        trap_toon, trap_gag = cog.trap
                    # TODO #10, Add chance_to_hit
                    attack_hit = toon.do_attack(target=cog, gag_atk=gag_atk,
                                                overdefeat=is_overdefeat)
                    # Attack doesn't miss and Gag is eligible for reward
                    if attack_hit:
                        # Activate the Trap Gag if the BattleEntity lures a trapped BattleEntity
                        if cog.is_lured and cog_is_trapped:
                            self.attacks.append((trap_toon, cog, trap_gag,
                                                 attack_hit))

                self.attacks.append((toon, target_cogs, gag_atk, attack_hit))

            for cog in self.context.cogs:
                if cog.is_defeated:
                    self.context.remove_cog(defeated_cog=cog)

        if all([cog.is_defeated for cog in self.context.cogs]):
            # ! First need to check if all cogs defeated, then battle is Won
            transition_state = WinState
        else:
            transition_state = CogAttackState
        self.context.transition_to(new_state=transition_state())


class CogAttackState(AttackState):

    def __init__(self):
        self.attacks = {}  # {BattleEntity: (BattleEntity, Damage)}

    def handle_attacks(self):
        transition_state = ToonAttackState

        for cog in self.context.cogs:
            cog_atk = cog.manual_atk if cog.manual_atk is not None else cog.choose_attack()  # noqa

            viable_toons = [toon for toon in self.context.toons
                            if not toon.is_defeated]
            if cog_atk.target == ATK_TGT_MULTI:
                print(f"        [+] {self} BattleEntity {cog} targets all Toons "
                      f"{viable_toons}")
                for toon in viable_toons:
                    atk_hit = cog.do_attack(target=toon, attack=cog_atk)
                    if toon.is_defeated:
                        print(f"            [-] BattleEntity {target_toon} is defeated")  # noqa
                        # ! If all Toons defeated -> LoseState else ToonAtkState  # noqa
                    self.attacks[cog] = (toon, cog_atk, atk_hit)

            else:
                # TODO #40, choose_target
                target_toon = rand_choice(viable_toons)
                print(f"        [+] {self} BattleEntity {cog} targets BattleEntity "
                      f"{target_toon}")
                atk_hit = cog.do_attack(target=target_toon, attack=cog_atk)
                self.attacks[cog] = (target_toon, cog_atk, atk_hit)

                if target_toon.is_defeated:
                    print(f"            [-] BattleEntity {target_toon} is defeated")
                    # ! If all Toons defeated -> LoseState else ToonAtkState

            if all([toon.is_defeated for toon in self.context.toons]):
                transition_state = LoseState
                break

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
    # TODO #37, #45: Implement methods to calculate rewards, remove BattleEntity's Gags
    # TODO #9, implement functionality & create tests for BattleEntity losing to BattleEntity

    # Need an __init__ function, otherwise it'll initialize as an WinLoseState
    def __init__(self):
        super()

    def handle_win_lose(self):
        # TODO #11, replace this double for-loop with Gag objects
        # TODO Alternatively, make BattleEntity.is_defeated a property, strip all the
        # Gags in the setter method if BattleEntity.is_defeated is True
        defeated_toons = [
            toon for toon in self.context._toons if toon.is_defeated]

        for toon in defeated_toons:
            print(f"        [-] Removing all Gags from BattleEntity {toon}")
            for track_idx, gag_track in enumerate(toon.gags):
                for gag_idx, gag in enumerate(toon.gags[track_idx]):
                    # Set the Gag count to 0 if the Gag is unlocked, or leave
                    # the Gag locked
                    toon.gags[track_idx][gag_idx] = 0 if gag != -1 else -1

        self.context.reward = [0]*7
        self.context.transition_to(new_state=EndState())


class EndState(BattleState):
    pass
