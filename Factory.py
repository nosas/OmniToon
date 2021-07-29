from .Cog import Cog
from .Entity import BattleEntity, Entity
from .Battle import BattleCog


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
            return BattleCogFactory.get_battle_entity(battle_id=battle_id, entity=entity)


class BattleCogFactory:

    def get_battle_entity(battle_id: int, entity: Entity) -> BattleCog:
        return BattleCog(battle_id=battle_id, entity=entity)


class LuredBattleCogFactory(BattleCogFactory):

    def get_battle_entity(battle_id: int, entity: Entity) -> BattleCog:
        bc = super().get_battle_entity(battle_id=battle_id, entity=entity)
        bc.is_lured = True
        return bc


class TrappedBattleCogFactory(BattleCogFactory):

    def get_battle_entity(battle_id: int, entity: Entity) -> BattleCog:
        bc = super().get_battle_entity(battle_id=battle_id, entity=entity)
        bc.is_trapped = True
        return bc
