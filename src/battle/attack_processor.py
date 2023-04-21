from typing import List, Union

from src.battle.attack import Attack
from src.battle.battle_entity import BattleEntity
from src.core.exceptions import InvalidTargetError, TargetDefeatedError


class AttackProcessor:
    def __init__(
        self,
        attacker: BattleEntity,
        attack: Attack,
        targets: List[BattleEntity],
    ):
        self.attacker = attacker
        self.attack = attack
        self.targets = targets

    def process(self):
        self.validate_targets()
        self.do_action(self.action)

    def validate_targets(self):
        for target in self.targets:
            if target.is_defeated:
                raise TargetDefeatedError(
                    f"Target {target.name} has already been defeated"
                )
            if target not in self.attack.targets:
                raise InvalidTargetError(
                    f"Target {target.name} is not a valid target for {self.attack.name}"
                )

    def do_action(self, action):
        if action == "attack":
            self.do_attack()
        elif action == "heal":
            self.do_heal()
        elif action == "pass":
            self.do_pass()
        else:
            raise ValueError(f"Invalid action: {action}")

    def do_attack(
        self,
        force_miss: bool = False,
        overdefeat: bool = False,
    ):
        # TODO #10, Add chance_to_hit
        attack_hit = False if force_miss else True
        hit_miss = "misses"
        damage = 0

        if attack_hit:
            hit_miss = "hits"
            damage = self.attack.damage

        for target in self.targets:
            if target.is_defeated and overdefeat is False:
                # Multiple Toons attack the same Cog with the same Gag track
                raise TargetDefeatedError(f"Cannot attack defeated {type(target)}")

            target_hp_before = target.hp
            target._get_attacked(amount=damage)
            class_name = type(self.attacker).__name__
            # TODO Add attack name and object name
            attack_name = self.attack.name
            print(
                f"            [-] {class_name} `do_attack()` ({attack_name=}) {self} "
                f"{self.attack.name} {hit_miss} {target} -> {target_hp_before}hp-"
                f"{damage}dmg"
            )

        return attack_hit

    def do_heal(self):
        for target in self.targets:
            target_hp_before = target.hp
            target._get_healed(amount=self.attack.damage)
            class_name = type(self.attacker).__name__
            # TODO Add attack name and object name
            attack_name = self.attack.name
            print(
                f"            [-] {class_name} `do_heal()` ({attack_name=}) {self} "
                f"{self.attack.name} heals {target} -> {target_hp_before}hp+"
                f"{self.attack.damage}hp"
            )
