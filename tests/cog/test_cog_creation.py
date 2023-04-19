from src.core.cog import Cog
from src.core.entity import Entity
from src.factories.utils import create_cog

KEY = "f"
NAME = "Flunky"


class TestCogFactoryCreation:
    cog = create_cog(key=KEY)
    expected_hp = 6
    expected_level = 1
    expected_rel_level = 0

    def test_hp(self):
        assert self.cog.hp == self.expected_hp

    def test_name(self):
        assert self.cog.name == NAME

    def test_key(self):
        assert self.cog.key == KEY

    def test_level(self):
        assert self.cog.level == self.expected_level

    def test_relative_level(self):
        assert self.cog.relative_level == self.expected_rel_level

    def test_type(self):
        assert isinstance(self.cog, Cog)
        assert isinstance(self.cog, Entity)
