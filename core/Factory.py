from Battle import BattleCog, ToonAttack
from Cog import Cog
from core.Entity import BattleEntity, Entity
from Gag import Gag, get_gag_min_max_exp
from Toon import Toon

from .GagGlobals import TRACK


class EntityFactory:

    def get_entity(self, name: str, hp: int) -> Entity:
        return Entity(name=name, hp=hp)


class CogFactory(EntityFactory):

    def get_entity(self, key: str, relative_level: int = 0) -> Entity:
        cog = self.get_cog(key=key, relative_level=relative_level)
        return super().get_entity(name=cog.name, hp=cog.hp)

    def get_cog(self, key: str, relative_level: int = 0) -> Cog:
        return Cog(key=key, relative_level=relative_level)


class BattleEntityFactory:

    # TODO : Increment battle_id for each new BattleCog
    def get_battle_entity(self, battle_id: int, entity: Entity) -> BattleEntity:
        if isinstance(entity, Cog):
            return BattleCogFactory.get_battle_cog(battle_id=battle_id, entity=entity)
        if isinstance(entity, Toon):
            raise NotImplementedError
        elif isinstance(entity, Entity):
            return BattleEntity(battle_id=battle_id, entity=entity)
        else:
            raise TypeError


class BattleCogFactory:

    @staticmethod
    def get_battle_cog(battle_id: int, entity: Entity,
                       lured: bool = False, trapped: bool = False) -> BattleCog:
        if lured and trapped:
            raise TypeError("BattleCogs cannot be trapped and lured")
        if lured:
            return LuredBattleCogFactory.get_battle_cog(battle_id=battle_id, entity=entity)
        if trapped:
            return TrappedBattleCogFactory.get_battle_cog(battle_id=battle_id, entity=entity)
        return BattleCog(battle_id=battle_id, entity=entity)


class LuredBattleCogFactory(BattleCogFactory):

    @staticmethod
    def get_battle_cog(battle_id: int, entity: Entity) -> BattleCog:
        bc = BattleCog(battle_id=battle_id, entity=entity)
        bc.is_lured = True
        return bc


class TrappedBattleCogFactory(BattleCogFactory):

    @staticmethod
    def get_battle_cog(battle_id: int, entity: Entity) -> BattleCog:
        bc = BattleCog(battle_id=battle_id, entity=entity)
        bc.is_trapped = True
        return bc


class GagFactory:

    @staticmethod
    def get_gag(track: TRACK, level: int = None, exp: int = None) -> Gag:
        if exp is None:
            exp = get_gag_min_max_exp(track=track, level=level)[0]
        return Gag(track=track, level=level, exp=exp)


class ToonAttackFactory:

    @staticmethod
    def get_toon_attack(gag: Gag, target_cog: BattleCog):
        return ToonAttack(gag=gag, target_cog=target_cog)
