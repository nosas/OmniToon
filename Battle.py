from .BattleState import BattleContext, EndState, ToonAttackState
from .Cog import Cog
from .Exceptions import TooManyGagsError, TooManyToonsError
from .GagGlobals import TRAP_TRACK
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
        return self.context.cogs

    @property
    def toons(self):
        return self.context.toons

    # TODO #49, Create negative test for adding new Toon/Cog
    def add_cog(self, new_cog: Cog):
        try:
            self.context.add_cog(new_cog)
        except TooManyGagsError as e:
            print(f"[!] ERROR : Cannot add Cog {new_cog}, too many Cogs")
            raise e

    def add_toon(self, new_toon: Toon):
        try:
            self.context.add_toon(new_toon)
            self._rewards[new_toon] = [0]*7
        except TooManyToonsError as e:
            print(f"    [!] ERROR : Too many Toons battling, can't add Toon "
                  f"{new_toon}")
            raise e

    def calculate_rewards(self) -> list:
        # import pprint  # To make rewards output readable
        # pp = pprint.PrettyPrinter(indent=1)
        print(f"[$] `calculate_rewards()` for all Toons")
        toon_attack_states = [
            state for state in self.context._completed_states if
            type(state) == ToonAttackState
        ]

        for attack_state in toon_attack_states:
            for toon, cog, gag, atk_hit in attack_state.attacks:
                # TODO #51, Multiply reward by EXP multiplier
                if atk_hit:
                    reward = gag.level + 1 if gag.level < cog.level else 0
                    if gag.track == TRAP_TRACK:  # Don't reward for Trap setup
                        if gag.is_setup and not gag.is_attack:
                            reward = 0
                else:  # Attack missed
                    reward = 0
                self._rewards[toon][gag.track] += reward
                print(f"    [>] {toon} {'+' if atk_hit else ''}{reward} {gag.track_name} exp ({gag}) against {cog}")  # noqa

        # Sum rewards for all Toons
        for toon in self.toons:
            print(f"    [+] `calculate_rewards()` for Toon {toon}")
            # If Toon is defeated, no rewards are given
            if toon.is_defeated:
                self._rewards[toon] = [0]*7
                continue
            print(f"        [-] Total rewards for Toon {toon} : "
                  f"{self._rewards[toon]}")
        print("    [-] `calculate_rewards()` all rewards ... ")
        # pp.pprint(self._rewards)
        return self._rewards

    def update(self):
        self.context.update()
        if type(self.context.state) == EndState:
            self.is_battling = False
