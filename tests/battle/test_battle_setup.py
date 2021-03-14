from ...Battle import Battle
from ..fixtures.cog_fixtures import cog_flunky
from ..fixtures.toon_fixtures import toon_astro


class TestBattleSetup:

    def test_battle_1toon_1cog(self, toon_astro, cog_flunky):
        print("*********************************")
        print(type(toon_astro), (type(cog_flunky)))
        first_battle = Battle(first_cog=cog_flunky, first_toon=toon_astro)
        # TODO Create __str__ functions for toons/cogs so they display
        # TODO some useful information when printing
        print(first_battle.toons)
        print(first_battle.cogs)
        # ! TODO Create tests for adding toon,cog, calculating rewards
        # ! TODO Create functionality for removing cog/toon if their hp <= 0
        # ! TODO Create functionality for removing all gags if toon.hp <= 0
        first_battle.update()
        print(first_battle.cogs[0].hp)
