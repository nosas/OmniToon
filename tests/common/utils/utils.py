from src.battle.battle import RewardCalculator, ToonAttack
from src.core.cog import Cog


def get_cog_from_request_param(request_param) -> Cog:
    """Given a pytest request containing a Cog or a (key, rel_lvl) tuple, return a Cog object

    Args:
        request_param (Cog | Tuple[str, int]): Cog object or a (key, rel_lvl) tuple

    Returns:
        Cog: Cog object
    """
    if isinstance(request_param, tuple):
        return Cog(key=request_param[0], relative_level=request_param[1])
    elif isinstance(request_param, Cog):
        return request_param
    else:
        raise TypeError(f"What the heck did you request? {request_param}")


def get_expected_reward(toon_attack: ToonAttack, rc: RewardCalculator) -> int:
    """Given a ToonAttack and RewardCalculator, return the expected reward value"""
    if toon_attack.gag.level >= toon_attack.target_cog.level:
        return -1
    else:
        return round(rc.get_base_reward(attack=toon_attack) * rc.get_multiplier())
