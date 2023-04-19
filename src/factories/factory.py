from random import choice as rand_choice
from random import randint

from src.battle.battle import BattleCog, ToonAttack
from src.core.cog import Cog
from src.core.cog_globals import COG_ATTRIBUTES
from src.core.entity import BattleEntity, Entity
from src.core.toon import Toon
from src.gags.gag import Gag, get_gag_min_max_exp
from src.gags.gag_globals import TRACK


class EntityFactory:
    def create_entity(self, name: str, hp: int) -> Entity:
        return Entity(name=name, hp=hp)


class CogFactory(EntityFactory):
    def create_entity(self, key: str, relative_level: int = 0) -> Entity:
        cog = self.create_cog(key=key, relative_level=relative_level)
        return super().create_entity(name=cog.name, hp=cog.hp)

    def create_cog(self, key: str, relative_level: int = 0) -> Cog:
        """Return a Cog, given a key and a relative level <= 4"""
        return Cog(key=key, relative_level=relative_level)


class RandomCogFactory(CogFactory):
    """Return a random Cog of a given, or random (by default), level"""

    def create_cog(self, key: str = None, relative_level: int = None) -> Cog:
        if key is None:
            key = rand_choice(list(COG_ATTRIBUTES.keys()))
        if relative_level is None:
            relative_level = randint(0, 4)
        return super().create_cog(key=key, relative_level=relative_level)


class BattleEntityFactory:
    # TODO : Increment battle_id for each new BattleCog
    def create_battle_entity(self, battle_id: int, entity: Entity) -> BattleEntity:
        if isinstance(entity, Cog):
            return BattleCogFactory.create_battle_cog(
                battle_id=battle_id, entity=entity
            )
        if isinstance(entity, Toon):
            raise NotImplementedError
        elif isinstance(entity, Entity):
            return BattleEntity(battle_id=battle_id, entity=entity)
        else:
            raise TypeError


class BattleCogFactory:
    @staticmethod
    def create_battle_cog(
        battle_id: int, entity: Entity, lured: bool = False, trapped: bool = False
    ) -> BattleCog:
        if lured and trapped:
            raise TypeError("BattleCogs cannot be trapped and lured")
        if lured:
            return LuredBattleCogFactory.create_battle_cog(
                battle_id=battle_id, entity=entity
            )
        if trapped:
            return TrappedBattleCogFactory.create_battle_cog(
                battle_id=battle_id, entity=entity
            )
        return BattleCog(battle_id=battle_id, entity=entity)


class LuredBattleCogFactory(BattleCogFactory):
    @staticmethod
    def create_battle_cog(battle_id: int, entity: Entity) -> BattleCog:
        bc = BattleCog(battle_id=battle_id, entity=entity)
        bc.is_lured = True
        return bc


class TrappedBattleCogFactory(BattleCogFactory):
    @staticmethod
    def create_battle_cog(battle_id: int, entity: Entity) -> BattleCog:
        bc = BattleCog(battle_id=battle_id, entity=entity)
        bc.is_trapped = True
        return bc


class GagFactory:
    @staticmethod
    def create_gag(track: TRACK, level: int = 0, exp: int = 0, count: int = 0) -> Gag:
        if exp == 0:
            exp = get_gag_min_max_exp(track=track, level=level)[0]
        return Gag(track=track, level=level, exp=exp, count=count)


class ToonAttackFactory:
    @staticmethod
    def create_toon_attack(gag: Gag, target_cog: BattleCog):
        return ToonAttack(gag=gag, target_cog=target_cog)
